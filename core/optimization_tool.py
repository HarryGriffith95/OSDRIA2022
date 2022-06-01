import re

from pyomo.environ import *
import pyomo.core.kernel.set_types as var_types
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from math import exp, pi

from PySide2.QtCore import QObject, Signal

from models.constants import DatasetResolution, PyomoVarType, DisplayType
from models.property import PropertyValueTimeSeries
from models.data_structure import List, Dict

SOLVER = 'gurobi'
# solver time limit in seconds
TIME_LIMIT = 60 * 2000


class Optimizer(QObject):
    """incorporates the optimization code of Pyomo"""
    progress_text_sent = Signal(str)

    def __init__(self, process_list, commodity_list):
        super().__init__()
        self._processes = process_list
        self._commodities = commodity_list
        self._model = self.init_model()
        self._commodity_list = {}
        self._variables = {}
        self._py_variables = {}
        self._objective_expressions = []

    def init_model(self):
        """Initialize optimization model including suffixes for sensitivity analysis"""
        model = ConcreteModel(name="OSDRIA optimization model")
        model.dual = Suffix(direction=Suffix.IMPORT)
        model.rc = Suffix(direction=Suffix.IMPORT)
        model.slack = Suffix(direction=Suffix.IMPORT)

        return model

    def relax(self):
        """Relaxation of model: make integers and boolean continuous"""
        for variable in self._model.component_data_objects(Var):
            variable.domain = NonNegativeReals

    def translate(self):
        """translate processes in pyomo code"""
        # perform process specific translation
        for process in self._processes:
            self.progress_text_sent.emit("Translating Process: " + process.name)
            process_code_name = process.name.lower().replace(" ", "_")
            obj = process.core.objective_function
            const = process.core.constraints
            [obj, const] = self.translate_variables(process_code_name, process.core.variables, obj, const)
            [obj, const] = self.translate_data(process.core.data, obj, const)
            [obj, const] = self.translate_properties(process_code_name, process.properties[1:], obj, const)
            [obj, const] = self.translate_commodities(process_code_name, process, obj, const)
            const = self.translate_precalculations(const)
            self.translate_constraints(process_code_name, const)
            self.translate_objective(process_code_name, obj)

        # add commodity constraints
        for commodity, content in self._commodity_list.items():
            self.progress_text_sent.emit("Translating Commodity: " + commodity)
            # create Constraint
            commodity_code_name = "commodity_" + commodity.lower().replace(" ", "_")
            res_index = "[_" + str(content['resolution'])[0].lower() + "_]"
            # set commodity sum to overflow variable
            pos_overflow = commodity_code_name + "_overflow_pos"
            neg_overflow = commodity_code_name + "_overflow_neg"
            commodity_const = content['com_sum'] + "==" + pos_overflow + res_index + " - " + neg_overflow + res_index
            commodity_range = range(content['resolution'].value)

            self._model.add_component(pos_overflow, Var(commodity_range, within=NonNegativeReals))
            self._variables[pos_overflow] = self._model.component(pos_overflow)
            self._model.add_component(neg_overflow, Var(commodity_range, within=NonNegativeReals))
            self._variables[neg_overflow] = self._model.component(neg_overflow)

            self.translate_constraints(commodity_code_name, commodity_const)

            commodity_objective = "(" + pos_overflow + res_index + " + " + neg_overflow + res_index + ") * 1000000"
            self.translate_objective(commodity_code_name, commodity_objective)

        # add objective function
        self.progress_text_sent.emit("Translating Objective Function")
        self._model.objective = Objective(expr=sum(self._objective_expressions))

    def solve(self, log_file):
        now = datetime.now().strftime('%Y%m%dT%H%M')
        log_file = log_file.split(".")[0] + now + ".log"

        solver = SolverFactory(SOLVER)
        if SOLVER == 'cplex':
            solver.options['timelimit'] = TIME_LIMIT
            solver.options['log'] = log_file
        elif SOLVER == 'glpk':
            solver.options['tmlim'] = TIME_LIMIT
            solver.options['log'] = log_file
        elif SOLVER == 'gurobi':
            solver.options['TimeLimit'] = TIME_LIMIT
            solver.options['logfile'] = log_file
            solver.options['NonConvex'] = 2

        results = solver.solve(self._model, tee=True)
        print(results)
        return results

    def write(self, filename):
        """Write model to file for external solver"""
        self._model.write(filename=filename.split(".")[0] + ".mps", io_options={'symbolic_solver_labels': True})

    def get_model(self, file):
        file_name = file.split(".")[0] + "_model_obj.txt"
        file = open(file_name, "w")
        """return model expressions"""
        # print("Variables")
        # model_expr = "Variables:\n"
        # for variable in self._model.component_data_objects(Var):
        #     model_expr += str(variable) + " ... " + str(variable.domain) + "\n"
        # print("Parameters")
        # model_expr += "Parameters:\n"
        # for parameter in self._model.component_data_objects(Param):
        #     model_expr += str(parameter) + "\n"
        # file.write("Constraints:\n")
        # for constraint in self._model.component_data_objects(Constraint):
        #     print(constraint.expr)
        #     file.write(str(constraint.expr) + "\n")
        file.write("Objective:\n")
        for expression in self._model.component_data_objects(Expression):
            print(expression.expr)
            file.write(str(expression.expr) + "\n")
        file.close()
        print("Done")

    def get_sensitivities(self, file):
        """get all types of sensitivities: duals, reduced costs, slacks"""
        file_name = file.split(".")[0] + "_sensitivity.txt"
        file = open(file_name, "w")
        #file.write("Duals:\n")
        #for key, item in self._model.dual.items():
        #    file.write(str(key) + ": " + str(item) + "\n")
        #file.write("Reduced costs:\n")
        #for key, item in self._model.rc.items():
        #    file.write(str(key) + ": " + str(item) + "\n")
        #file.write("Slacks:\n")
        #for key, item in self._model.slack.items():
        #    file.write(str(key) + ": " + str(item) + "\n")
        file.close()

    def set_results(self):
        """set optimization results in processes and commodities"""
        for process in self._processes:
            process.optimization_output = Dict({})
            process_code_name = process.name.lower().replace(" ", "_")
            for variable in process.core.variables:
                if variable.type is not PyomoVarType.NON_PYOMO:
                    variable_code_name = variable.name.lower().replace(" ", "_")
                    unique_name = process_code_name + "__" + variable_code_name
                    result_list = list(self._model.component(unique_name).get_values().values())
                    # check for None values
                    process.optimization_output[variable.name] = List([result for result in result_list
                                                                       if result is not None])

        # set commodity flow results
        for commodity in self._commodities:
            commodity.optimization_output = Dict({"input_processes": Dict({}), "output_processes": Dict({})})
            in_out_commodities = [str(process)
                                  for process in self._commodity_list[commodity.name]["input_processes"]
                                  if process in self._commodity_list[commodity.name]["output_processes"]]
            commodity_code_name = commodity.name.lower().replace(" ", "_")
            input_com = True
            for process_direction in ["input_processes", "output_processes"]:
                for process_name in self._commodity_list[commodity.name][process_direction]:
                    process_code_name = process_name.lower().replace(" ", "_")
                    commodity_process_name = commodity_code_name
                    if process_name in in_out_commodities:
                        commodity_process_name += "_in" if input_com else "_out"
                    commodity_process_name += "__" + process_code_name
                    result_list = self._model.component(commodity_process_name).get_values().values()
                    commodity.optimization_output[process_direction][process_name] = \
                        List([result for result in result_list if result is not None])
                # add balance to commodity flows
                if input_com:
                    commodity_process_name = "commodity_" + commodity_code_name + "_overflow_pos"
                    process_name = "Positive Balance"
                else:
                    commodity_process_name = "commodity_" + commodity_code_name + "_overflow_neg"
                    process_name = "Negative Balance"

                result_list = list(self._model.component(commodity_process_name).get_values().values())
                # check result_list for None values
                commodity.optimization_output[process_direction][process_name] = List([result for result in result_list
                                                                                       if result is not None])
                input_com = False

    def cancel(self):
        pass

    def translate_variables(self, process_code_name, variables, obj, const):
        # converts variables into pyomo variables and adds them to list
        for variable in variables:
            variable_code_name = variable.name.lower().replace(" ", "_")
            unique_name = process_code_name + "__" + variable_code_name
            replace_name = unique_name

            # add variable to declaration as pyomo Var
            pyomo_type = variable.type
            if pyomo_type.name in [res.name for res in list(DatasetResolution)]:
                # set boundaries for index variables
                resolution = DatasetResolution[pyomo_type.name]
                pyomo_type = PyomoVarType.NON_NEGATIVE_INTEGERS
                self._model.add_component(unique_name, Var(within=getattr(var_types, pyomo_type.value),
                                                           bounds=(0, resolution.value - 1)))

            else:
                # only add new component if it is a pyomo variable
                if pyomo_type is not PyomoVarType.NON_PYOMO:
                    self._model.add_component(unique_name, Var(range(variable.resolution.value),
                                                               within=getattr(var_types, pyomo_type.value)))
                # replace indexed variable name
                [obj, const] = self.translate_indexed_terms([obj, const],
                                                            variable_code_name, unique_name,
                                                            variable.resolution)
                replace_name += "[_" + str(variable.resolution)[0].lower() + "_]"

            # replace variable name without indexing
            re_pattern = re.compile(r"\b(" + re.escape(variable_code_name) + r")(\b[^\[]|$)", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, replace_name + r"\g<2>", s) for s in [obj, const]]

            # distinguish between pyomo and non-pyomo variables by different lists
            if pyomo_type is PyomoVarType.NON_PYOMO:
                self._py_variables[unique_name] = variable.resolution.value
            else:
                self._variables[unique_name] = self._model.component(unique_name)

        return [obj, const]

    @staticmethod
    def translate_data(data, obj, const):
        # replaces data name with number
        for datum in data:
            datum_name = datum.name.lower().replace(" ", "_")
            [obj, const] = [s.replace(datum_name, datum.value) for s in [obj, const]]

        return [obj, const]

    def translate_properties(self, process_code_name, properties, obj, const):
        # replaces property names with number or create pyomo Param for time series
        for prop in properties:
            prop_code_name = prop.name.lower().replace(" ", "_")
            if isinstance(prop.value, PropertyValueTimeSeries):
                unique_name = process_code_name + "__" + prop_code_name
                init_dict = {i: float(v) for i, v in enumerate(prop.value.value)}
                resolution = DatasetResolution(len(prop.value.value))
                # add property to declaration as pyomo Param
                self._model.add_component(unique_name, Param(range(resolution.value), initialize=init_dict))
                self._variables[unique_name] = self._model.component(unique_name)
                # replace indexed variable name
                [obj, const] = self.translate_indexed_terms([obj, const], prop_code_name, unique_name, resolution)

                unique_name += "[_" + str(resolution)[0].lower() + "_]"
            else:
                unique_name = str(prop.value)

            re_pattern = re.compile(r"\b(" + re.escape(prop_code_name) + r")(\b[^\[]|$)", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, unique_name + r"\g<2>", s) for s in [obj, const]]

        return [obj, const]

    def translate_commodities(self, process_code_name, process, obj, const):
        # converts commodities into pyomo variables and adds them to list respecting the direction
        in_out_commodities = [str(commodity) for commodity in process.inputs if commodity in process.outputs]

        input_com = True
        for commodities in [process.inputs, process.outputs]:
            for commodity in commodities:
                commodity_code_name = commodity.name.lower().replace(" ", "_")
                if str(commodity) in in_out_commodities:
                    commodity_code_name += "_in" if input_com else "_out"
                unique_name = commodity_code_name + "__" + process_code_name
                if commodity.name not in self._commodity_list:
                    self._commodity_list[commodity.name] = {'resolution': commodity.resolution, 'com_sum': "",
                                                            'input_processes': [], 'output_processes': []}

                # get original resolution of commodity from process core
                core_commodities = process.core.inputs if input_com else process.core.outputs
                core_commodity = [com for com in core_commodities if str(com) == commodity.name][0]
                core_commodity_resolution = core_commodity.resolution

                # set resolution of commodity sum to highest of all process commodity resolutions
                if core_commodity_resolution.value > self._commodity_list[commodity.name]['resolution'].value:
                    self._commodity_list[commodity.name]['resolution'] = core_commodity_resolution

                # add variable to declaration as pyomo Var
                self._model.add_component(unique_name, Var(range(core_commodity_resolution.value),
                                                           within=NonNegativeReals))
                self._variables[unique_name] = self._model.component(unique_name)

                # replace indexed variable name
                [obj, const] = self.translate_indexed_terms([obj, const], commodity_code_name, unique_name,
                                                            core_commodity_resolution)
                # replace commodity name without indexing
                resolution_index = "[_" + str(core_commodity_resolution)[0].lower() + "_]"
                re_pattern = re.compile(r"\b(" + re.escape(commodity_code_name) + r")(\b[^\[]|$)", flags=re.MULTILINE)
                [obj, const] = [re.sub(re_pattern, unique_name + resolution_index + r"\g<2>", s) for s in [obj, const]]

                # and commodity with -/+ as input/output to commodity sum
                commodity_direction = '-' if input_com else '+'
                self._commodity_list[commodity.name]['com_sum'] += commodity_direction + unique_name + resolution_index

                process_direction = 'input_processes' if input_com else 'output_processes'
                self._commodity_list[commodity.name][process_direction].append(process.name)
            input_com = False

        return [obj, const]

    def translate_precalculations(self, const):
        for line in const.split("\n"):
            # search for constraint line with specific pattern: variable[index] = formula
            re_pattern = re.compile(r"^\s*(.*?)\[.*?\]\s*=\s*([^=]*?)$")
            match = re.search(re_pattern, line)

            if not match:
                # jump to next line
                continue
            elif match[1] in self._py_variables.keys():
                # erase line from constraints
                const = const.replace(line + "\n", "")

                py_variable = match[1]
                # create new parameter with definition by line
                resolution_value = self._py_variables[py_variable]
                self._model.add_component(py_variable,
                                          Param(range(resolution_value),
                                                initialize={i: eval(match[2], {**self._variables, **self._py_variables},
                                                                    {"_h_": int(i * 8760 / resolution_value),
                                                                     "_d_": int(i * 365 / resolution_value),
                                                                     "_w_": int(i * 52 / resolution_value),
                                                                     "_m_": int(i * 12 / resolution_value),
                                                                     "_y_": 0,
                                                                     "_i_": i,
                                                                     "exp": exp}) for i in range(resolution_value)}))
                self._py_variables[py_variable] = self._model.component(py_variable)

        return const

    def translate_constraints(self, process_code_name, const):
        for index, constraint in enumerate(const.split("\n")):
            # skip empty lines
            if constraint.strip() == "":
                continue
            unique_name = process_code_name + "__const_" + str(index)
            constraint = constraint.replace("[_y_]", "[0]")
            single_resolution = True

            for resolution in list(DatasetResolution):
                resolution_letter = "_" + str(resolution)[0].lower() + "_"
                if resolution_letter in constraint:
                    constraint = self.translate_piecewise_constraint(constraint, unique_name, resolution)
                    self._model.add_component(unique_name,
                                              Constraint(range(resolution.value),
                                                         rule=lambda model, i:
                                                         eval(constraint, {**self._variables, **self._py_variables},
                                                              {"_h_": int(i * 8760 / resolution.value),
                                                               "_d_": int(i * 365 / resolution.value),
                                                               "_w_": int(i * 52 / resolution.value),
                                                               "_m_": int(i * 12 / resolution.value)})))
                    single_resolution = False
                    break

            if single_resolution:
                self._model.add_component(unique_name, Constraint(expr=eval(constraint,
                                                                            {**self._variables, **self._py_variables})))

    def translate_piecewise_constraint(self, constraint, unique_name, resolution):
        resolution_value = resolution.value
        res_index = "_" + str(resolution)[0].lower() + "_"
        piecewise_function_name = unique_name + "_piecewise_function"
        piecewise_output_name = unique_name + "_piecewise_output"
        piecewise_input_name = unique_name + "_piecewise_input"
        re_pattern = re.compile(r"\bPiecewise\(\s*(.*?)\s*,\s*({.*?\})\s*\)", flags=re.MULTILINE)

        piecewise_counter = 0
        # search for multiply Piecewise expressions in constraint line
        while True:
            match = re.search(re_pattern, constraint)
            if not match:
                break

            piecewise_counter += 1
            output_name = piecewise_output_name + "_" + str(piecewise_counter)
            function_name = piecewise_function_name + "_" + str(piecewise_counter)
            input_name = piecewise_input_name + "_" + str(piecewise_counter)

            constraint = re.sub(match.re, output_name + "[" + res_index + "]", constraint, 1)
            input_expression = match[1]
            data_dict = eval(match[2])
            indizes = list(data_dict.keys())

            # add input and output variables
            self._model.add_component(input_name, Var(range(resolution_value),
                                                      within=Reals,
                                                      bounds=(min(indizes), max(indizes))))
            self._model.add_component(output_name, Var(range(resolution_value), within=NonNegativeReals))
            self._variables[output_name] = self._model.component(output_name)

            # add constraint for relationship between input expression of Piecewise function
            # and actual input in piecewise function
            def input_constraint(model, i):
                return model.component(input_name)[i] == eval(input_expression,
                                                              {**self._variables, **self._py_variables},
                                                              {res_index: i})

            self._model.add_component(input_name + "_const", Constraint(range(resolution_value), rule=input_constraint))

            # add piecewise function with data_dict
            self._model.add_component(function_name, Piecewise(range(resolution_value),
                                                               self._model.component(output_name),
                                                               self._model.component(input_name),
                                                               pw_pts=indizes, pw_constr_type="EQ",
                                                               f_rule=list(data_dict.values())))

        return constraint

    def translate_objective(self, process_code_name, obj):
        if obj == "":
            return

        for index, objective_term in enumerate(obj.split("++")):
            unique_name = process_code_name + "__objective_term_" + str(index)
            term = objective_term.strip()
            term = term.replace("[_y_]", "[0]")
            single_resolution = True

            for resolution in list(DatasetResolution):
                resolution_letter = "_" + str(resolution)[0].lower() + "_"
                if resolution_letter in term:
                    self._model.add_component(unique_name,
                                              Expression(expr=sum(
                                                  eval(term,
                                                       {**self._variables, **self._py_variables},
                                                       {resolution_letter: i})
                                                  for i in range(resolution.value))))
                    single_resolution = False
                    break

            if single_resolution:
                self._model.add_component(unique_name, Expression(expr=eval(term,
                                                                            {**self._variables, **self._py_variables})))

            self._objective_expressions.append(self._model.component(unique_name))

    def translate_indexed_terms(self, string_list, code_name, unique_name, resolution):
        # pattern without +/- in index
        re_pattern_single_indexed = re.compile(r"\b" + re.escape(code_name) + r"\[([^:+-].*?)\]", flags=re.MULTILINE)
        # pattern with +/- in index
        re_pattern_index_shift = re.compile(r"\b" + re.escape(code_name) + r"\[([+-])(.*?)\]", flags=re.MULTILINE)

        for index, string in enumerate(string_list):
            match_single_indexed = re.search(re_pattern_single_indexed, string)
            match_index_shift = re.search(re_pattern_index_shift, string)

            # check which pattern applies and execute corresponding translation
            if match_single_indexed:
                string_list[index] = self.translate_single_indexed_term(string, match_single_indexed, unique_name)
            elif match_index_shift:
                string_list[index] = self.translate_index_shift_term(string, match_index_shift, unique_name, resolution)
            else:
                # jump to next for loop iteration
                continue

        return string_list

    def translate_single_indexed_term(self, string, match, unique_name):
        index_variable = match[1]
        # no replacement for numbers as index
        if index_variable.isdigit():
            return string

        piecewise_function_name = unique_name + "_function"
        piecewise_output_name = unique_name + "_output"
        # replace index parameter with list output variable
        string = re.sub(match.re, piecewise_output_name, string)
        # add list output variable
        self._model.add_component(piecewise_output_name, Var())
        self._variables[piecewise_output_name] = self._model.component(piecewise_output_name)
        # add piecewise function
        self._model.add_component(piecewise_function_name,
                                  Piecewise(self._model.component(piecewise_output_name),
                                            self._model.component(index_variable),
                                            pw_pts=list(self._model.component(unique_name).keys()),
                                            pw_constr_type="EQ",
                                            f_rule=list(self._model.component(unique_name).values())))

        return string

    def translate_index_shift_term(self, string, match, unique_name, resolution):
        index_sign = match[1]
        index_variable = match[2]
        res_index = "_" + str(resolution)[0].lower() + "_"

        # index shift is a parameter
        if index_variable.isdigit():
            full_index = "(" + res_index + index_sign + index_variable + ")%" + str(resolution.value)
            return re.sub(match.re, unique_name + "[" + full_index + "]", string)

        # index shift is a variable
        # todo create translation for index shifts
        return string