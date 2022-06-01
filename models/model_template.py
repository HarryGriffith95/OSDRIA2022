from PySide2.QtGui import QIcon, QPixmap

from models.property import *
from models.data_structure import List
from models.scenario import Scenario
from models.elements import Elements
from models.element import *
from models.constants import *


class ModelTemplate(object):
    """initialising values for model"""

    @staticmethod
    def overview_properties():
        project_name = PropertyLineEdit(
            "Project Name",
            "Name")
        project_longitude = PropertyLineEdit("Longitude", "0.0", "")
        project_latitude = PropertyLineEdit("Latitude", "0.0", "")
        project_location = PropertyDialog(
            "Project Location",
            List([project_longitude, project_latitude]))
        project_area = PropertyLineEdit(
            "Project Area",
            "0.0",
            "ha")
        property_list = List([project_name, project_location, project_area])

        return property_list

    @staticmethod
    def project_elements():
        return Elements([], [])

    @staticmethod
    def scenarios():
        scenario_1 = Scenario("1", List())
        scenario_2 = Scenario("2", List())
        scenario_3 = Scenario("3", List())
        scenario_4 = Scenario("4", List())
        scenario_list = PropertyPopupMenu("Scenarios", List([scenario_1,
                                                             scenario_2,
                                                             scenario_3,
                                                             scenario_4]))

        return scenario_list

    @staticmethod
    def process_cores(commodity_types, time_series):
        pv_core = ProcessCore()
        pv_core.name = "PV"
        pv_core.icon = QIcon(QPixmap(":/icons/img/photovoltaics@2x.png"))
        pv_core.category = ProcessCategory.PROCESS
        pv_core.section = OverviewSelection.ENERGY
        pv_core.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS,
                             "", DisplayType.YES),
            PropertyVariable("Shunt", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS)
        ])
        pv_core.data = List([PropertyValue("WACC", "0.15")])
        pv_core.properties = List([
            PropertyPopupMenu("Irradiation", time_series),
            PropertyLineEdit("Rated Power", "0.25", "kW"),
            PropertyLineEdit("Life Time", "25", "a"),
            PropertyLineEdit("Investment Costs", "1676", "$/kW"),
            PropertyLineEdit("Fixed Costs", "81", "$/kW"),
            PropertyLineEdit("Variable Costs", "0", "$/kWh")
        ])
        pv_core.outputs = List([Commodity("Electricity", commodity_types[0], DatasetResolution.HOURLY)])
        pv_core.objective_function = "amount * rated_power * " \
                                     "(investment_costs * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc) " \
                                     "+ fixed_costs) ++ electricity * variable_costs"
        pv_core.constraints = "electricity + shunt == amount * rated_power * irradiation"

        diesel_core = ProcessCore()
        diesel_core.name = "Diesel Generator"
        diesel_core.icon = QIcon(QPixmap(":/icons/img/diesel_generator@2x.png"))
        diesel_core.category = ProcessCategory.PROCESS
        diesel_core.section = OverviewSelection.ENERGY
        diesel_core.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS,
                             "", DisplayType.YES)
        ])
        diesel_core.data = List([PropertyValue("WACC", "0.15"),
                                 PropertyValue("Energy Density", "10", "kWh/l"),])
        diesel_core.properties = List([
            PropertyLineEdit("Efficiency", "0.28", ""),
            PropertyLineEdit("Rated Power", "5", "kW"),
            PropertyLineEdit("Life Time", "23", "a"),
            PropertyLineEdit("Investment Costs", "324", "$/kW"),
            PropertyLineEdit("Fixed Costs", "26.9", "$/kW"),
            PropertyLineEdit("Variable Costs", "0.01", "$/kWh")
        ])
        diesel_core.inputs = List([Commodity("Diesel", commodity_types[1], DatasetResolution.HOURLY)])
        diesel_core.outputs = List([Commodity("Electricity", commodity_types[0], DatasetResolution.HOURLY)])
        diesel_core.objective_function = "amount * rated_power * " \
                                         "(investment_costs * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc) " \
                                         "+ fixed_costs) ++ electricity * variable_costs"
        diesel_core.constraints = """electricity <= amount * rated_power
        electricity == diesel * energy_density * efficiency"""

        diesel_market_core = ProcessCore()
        diesel_market_core.name = "Diesel Market"
        diesel_market_core.icon = QIcon(QPixmap(":/icons/img/fuel_market@2x.png"))
        diesel_market_core.category = ProcessCategory.SUPPLY
        diesel_market_core.section = OverviewSelection.ENERGY
        diesel_market_core.properties = List([PropertyLineEdit("Diesel Price", "1.06", "$/l")])
        diesel_market_core.outputs = List([Commodity("Diesel", commodity_types[1], DatasetResolution.HOURLY)])
        diesel_market_core.objective_function = "diesel_price * diesel"

        biowaste_market_core = ProcessCore()
        biowaste_market_core.name = "Biowaste Market"
        biowaste_market_core.icon = QIcon(QPixmap(":/icons/img/bio_waste@2x.png"))
        biowaste_market_core.category = ProcessCategory.SUPPLY
        biowaste_market_core.section = OverviewSelection.BUSINESS
        biowaste_market_core.properties = List([
            PropertyLineEdit("Maize Straw Price", "500", "$/kg"),
            PropertyLineEdit("Chicken Manure Price", "500", "$/kg"),
            PropertyLineEdit("Pig Manure Price", "500", "$/kg")
        ])
        biowaste_market_core.outputs = List([
            Commodity("Maize Straw", commodity_types[3], DatasetResolution.HOURLY),
            Commodity("Chicken Manure", commodity_types[3], DatasetResolution.HOURLY),
            Commodity("Pig Manure", commodity_types[3], DatasetResolution.HOURLY)
        ])
        biowaste_market_core.objective_function = "maize_straw_price * maize_straw " \
                                                  "++ chicken_manure_price * chicken_manure " \
                                                  "++ pig_manure_price * pig_manure"
        food_market = ProcessCore()
        food_market.name = "Food Market"
        food_market.icon = QIcon(QPixmap(":/icons/img/food_market@2x.png"))
        food_market.category = ProcessCategory.DEMAND
        food_market.section = OverviewSelection.BUSINESS
        food_market.properties = List([
            PropertyLineEdit("Maize Sell Price", "0.5", "$/kg")
        ])
        food_market.inputs = List([
            Commodity("Maize", commodity_types[5], DatasetResolution.HOURLY)
        ])
        food_market.objective_function = "- maize_sell_price * maize"

        digester_core = ProcessCore()
        digester_core.name = "Biogas Digester"
        digester_core.icon = QIcon(QPixmap(":/icons/img/biogas_plant@2x.png"))
        digester_core.category = ProcessCategory.PROCESS
        digester_core.section = OverviewSelection.ENERGY
        digester_core.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS,
                             "", DisplayType.YES),
            PropertyVariable("Carbon", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Hydrogen", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Oxygen", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Nitrogen", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Sulphur", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_REALS)
        ])
        digester_core.data = List([
            PropertyValue("WACC", "0.15"),
            PropertyValue("Carbon MS", "0.39961"),
            PropertyValue("Hydrogen MS", "0.05462"),
            PropertyValue("Oxygen MS", "0.52694"),
            PropertyValue("Nitrogen MS", "0.01441"),
            PropertyValue("Sulphur MS", "0.00461"),
            PropertyValue("Water MS", "0.00006"),
            PropertyValue("Carbon CM", "0.07609"),
            PropertyValue("Hydrogen CM", "0.01334"),
            PropertyValue("Oxygen CM", "0.08046"),
            PropertyValue("Nitrogen CM", "0.00877"),
            PropertyValue("Sulphur CM", "0.00106"),
            PropertyValue("Water CM", "0.00075"),
            PropertyValue("Carbon PM", "0.1435"),
            PropertyValue("Hydrogen PM", "0.0193"),
            PropertyValue("Oxygen PM", "0.1191"),
            PropertyValue("Nitrogen PM", "0.0144"),
            PropertyValue("Sulphur PM", "0.0029"),
            PropertyValue("Water PM", "0.0005"),
        ])
        digester_core.properties = List([
            PropertyLineEdit("Rated Power", "0.2", "m3/h"),
            PropertyLineEdit("Life Time", "20", "a"),
            PropertyLineEdit("Investment Costs", "4512", "$/(m3/h)"),
            PropertyLineEdit("Fixed Costs", "362", "$/(m3/h)"),
            PropertyLineEdit("Variable Costs", "0", "$/m3")
        ])
        digester_core.inputs = List([
            Commodity("Maize Straw", commodity_types[3], DatasetResolution.YEARLY),
            Commodity("Chicken Manure", commodity_types[3], DatasetResolution.YEARLY),
            Commodity("Pig Manure", commodity_types[3], DatasetResolution.YEARLY),
            Commodity("Water", commodity_types[4], DatasetResolution.YEARLY)
        ])
        digester_core.outputs = List([
            Commodity("CH4", commodity_types[2], DatasetResolution.YEARLY),
            Commodity("CO2", commodity_types[2], DatasetResolution.YEARLY),
            Commodity("NH3", commodity_types[2], DatasetResolution.YEARLY),
            Commodity("H2S", commodity_types[2], DatasetResolution.YEARLY),
            Commodity("Water", commodity_types[4], DatasetResolution.YEARLY)
        ])
        digester_core.objective_function = "amount * rated_power * " \
                                           "(investment_costs * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc) " \
                                           "+ fixed_costs) ++ 8760 * (ch4 + co2 + nh3 + h2s) * variable_costs"
        digester_core.constraints = """
        carbon == carbon_ms * maize_straw + carbon_cm * chicken_manure + carbon_pm * pig_manure
        hydrogen == hydrogen_ms * maize_straw + hydrogen_cm * chicken_manure + hydrogen_pm * pig_manure
        oxygen == oxygen_ms * maize_straw + oxygen_cm * chicken_manure + oxygen_pm * pig_manure
        nitrogen == nitrogen_ms * maize_straw + nitrogen_cm * chicken_manure + nitrogen_pm * pig_manure
        sulphur == sulphur_ms * maize_straw + sulphur_cm * chicken_manure + sulphur_pm * pig_manure
        water_ms * maize_straw + water_cm * chicken_manure + water_pm * pig_manure + water_in - water_out >= (maize_straw + chicken_manure + pig_manure) * 0.3  
        carbon >= 20 * nitrogen
        carbon <= 30 * nitrogen
        ch4 == 0.930645204 * carbon + 2.772522162 * hydrogen - 0.349324969 * oxygen - 0.598518942 * nitrogen - 0.174297526 * sulphur
        co2 == 0.927066656 * carbon - 2.761861167 * hydrogen + 0.347981733 * oxygen + 0.596217497 * nitrogen + 0.173627311 * sulphur
        nh3 == 1.576155953 * nitrogen
        h2s == 0.691998896 * sulphur
        (ch4 + co2 + nh3 + h2s) <= amount * rated_power
        """

        biogas_gen_core = ProcessCore()
        biogas_gen_core.name = "Biogas Generator"
        biogas_gen_core.icon = QIcon(QPixmap(":/icons/img/biogas_generator@2x.png"))
        biogas_gen_core.category = ProcessCategory.PROCESS
        biogas_gen_core.section = OverviewSelection.ENERGY
        biogas_gen_core.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS,
                             "", DisplayType.YES)
            ])
        biogas_gen_core.data = List([PropertyValue("WACC", "0.15"),
                                     PropertyValue("Energy Density", "10", "kWh/m3")])
        biogas_gen_core.properties = List([
            PropertyLineEdit("Efficiency", "0.3", ""),
            PropertyLineEdit("Rated Power", "5", "kW"),
            PropertyLineEdit("Life Time", "23", "a"),
            PropertyLineEdit("Investment Costs", "652", "$/kW"),
            PropertyLineEdit("Fixed Costs", "26.9", "$/kW"),
            PropertyLineEdit("Variable Costs", "0.01", "$/kWh")
        ])
        biogas_gen_core.inputs = List([
            Commodity("CH4", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("CO2", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("NH3", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("H2S", commodity_types[2], DatasetResolution.HOURLY)
        ])
        biogas_gen_core.outputs = List([Commodity("Electricity", commodity_types[0], DatasetResolution.HOURLY)])
        biogas_gen_core.objective_function = "amount * rated_power * " \
                                         "(investment_costs * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc) " \
                                         "+ fixed_costs) ++ electricity * variable_costs"
        biogas_gen_core.constraints = """electricity <= amount * rated_power
                electricity == ch4 * energy_density * efficiency"""

        battery_core = ProcessCore()
        battery_core.name = "Battery"
        battery_core.icon = QIcon(QPixmap(":/icons/img/battery@2x.png"))
        battery_core.category = ProcessCategory.STORAGE
        battery_core.section = OverviewSelection.ENERGY
        battery_core.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS,
                             "", DisplayType.YES),
            PropertyVariable("Content", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS)
            ])
        battery_core.data = List([PropertyValue("WACC", "0.15")])
        battery_core.properties = List([
            PropertyLineEdit("Efficiency", "0.877", ""),
            PropertyLineEdit("Rated Power", "5", "kWh"),
            PropertyLineEdit("Life Time", "7.7", "a"),
            PropertyLineEdit("Investment Costs", "437", "$/kWh"),
            PropertyLineEdit("Fixed Costs", "30", "$/kWh")
        ])
        battery_core.inputs = List([Commodity("Electricity", commodity_types[0], DatasetResolution.HOURLY)])
        battery_core.outputs = List([Commodity("Electricity", commodity_types[0], DatasetResolution.HOURLY)])
        battery_core.objective_function = "amount * rated_power * " \
                                         "(investment_costs * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc) " \
                                         "+ fixed_costs)"
        battery_core.constraints = """
        content == content[-1] + electricity_in * efficiency - electricity_out / efficiency
        content <= amount * rated_power
        """

        biogas_tank_core = ProcessCore()
        biogas_tank_core.name = "Biogas Tank"
        biogas_tank_core.icon = QIcon(QPixmap(":/icons/img/biogas_tank@2x.png"))
        biogas_tank_core.category = ProcessCategory.STORAGE
        biogas_tank_core.section = OverviewSelection.ENERGY
        biogas_tank_core.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS,
                             "", DisplayType.YES),
            PropertyVariable("Content", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS)
        ])
        biogas_tank_core.data = List([PropertyValue("WACC", "0.15")])
        biogas_tank_core.properties = List([
            PropertyLineEdit("Size", "5", "m3"),
            PropertyLineEdit("Life Time", "10", "a"),
            PropertyLineEdit("Investment Costs", "19", "$/m3"),
            PropertyLineEdit("Fixed Costs", "0", "$/m3"),
            PropertyLineEdit("Variable Costs", "0", "$/m3")
        ])
        biogas_tank_core.inputs = List([
            Commodity("CH4", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("CO2", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("NH3", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("H2S", commodity_types[2], DatasetResolution.HOURLY)
        ])
        biogas_tank_core.outputs = List([
            Commodity("CH4", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("CO2", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("NH3", commodity_types[2], DatasetResolution.HOURLY),
            Commodity("H2S", commodity_types[2], DatasetResolution.HOURLY)
        ])
        biogas_tank_core.objective_function = "amount * size * " \
                                             "(investment_costs * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc) " \
                                             "+ fixed_costs)"
        biogas_tank_core.constraints = """
                content == content[-1] + ch4_in / 0.6 - ch4_out / 0.6
                co2_in == 0.3/0.6 * ch4_in
                co2_out == 0.3/0.6 * ch4_out
                nh3_in == 0.0995/0.6 * ch4_in
                nh3_out == 0.0995/0.6 * ch4_out
                h2s_in == 0.0005/0.6 * ch4_in
                h2s_out == 0.0005/0.6 * ch4_out
                content <= amount * size
                """

        electrical_demand_core = ProcessCore()
        electrical_demand_core.name = "Village Demand"
        electrical_demand_core.icon = QIcon(QPixmap(":/icons/img/demand@2x.png"))
        electrical_demand_core.category = ProcessCategory.DEMAND
        electrical_demand_core.section = OverviewSelection.ENERGY
        electrical_demand_core.properties = List([PropertyPopupMenu("Demand", time_series)])
        electrical_demand_core.inputs = List([Commodity("Electricity", commodity_types[0], DatasetResolution.HOURLY)])
        electrical_demand_core.constraints = "electricity == demand"

        water_pump = ProcessCore()
        water_pump.name = "Water Pump"
        water_pump.icon = QIcon(QPixmap(":/icons/img/water_pump@2x.png"))
        water_pump.category = ProcessCategory.PROCESS
        water_pump.section = OverviewSelection.WATER
        water_pump.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS,
                             "", DisplayType.YES)
            ])
        water_pump.data = List([
            PropertyValue("WACC", "0.15"),
            PropertyValue("Water Density", "1000", "kg/m3"),
            PropertyValue("Gravitation", "9.81", "m/s2")
        ])
        water_pump.properties = List([
            PropertyLineEdit("Rated Power", "5", "m3/h"),
            PropertyLineEdit("Efficiency", "0.5"),
            PropertyLineEdit("Total Dynamic Head", "38.1", "m"),
            PropertyLineEdit("Life Time", "25", "a"),
            PropertyLineEdit("Investment Costs", "1000", "$/(m3/h)"),
            PropertyLineEdit("Fixed Costs", "80", "$/(m3/h)"),
            PropertyLineEdit("Variable Costs", "0.1", "$/m3")
        ])
        water_pump.inputs = List([
            Commodity("Groundwater", commodity_types[4], DatasetResolution.HOURLY),
            Commodity("Electricity", commodity_types[0], DatasetResolution.HOURLY)
        ])
        water_pump.outputs = List([
            Commodity("Water", commodity_types[4], DatasetResolution.HOURLY)
            ])
        water_pump.objective_function = "amount * rated_power * (" \
                                        "investment_costs * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc)" \
                                        " + fixed_costs) ++ water * variable_costs"
        water_pump.constraints = """
        electricity * efficiency * 1000000 == water_density * gravitation * total_dynamic_head * water
        water == groundwater
        water <= amount * rated_power
        """

        village_water_demand = ProcessCore()
        village_water_demand.name = "Village Water Demand"
        village_water_demand.icon = QIcon(QPixmap(":/icons/img/demand@2x.png"))
        village_water_demand.category = ProcessCategory.DEMAND
        village_water_demand.section = OverviewSelection.WATER
        village_water_demand.properties = List([
            PropertyPopupMenu("Demand", time_series)
        ])
        village_water_demand.inputs = List([
            Commodity("Water", commodity_types[4], DatasetResolution.HOURLY)
        ])
        village_water_demand.constraints = "demand == water"

        aquifer = ProcessCore()
        aquifer.name = "Aquifer"
        aquifer.icon = QIcon(QPixmap(":/icons/img/aquifer@2x.png"))
        aquifer.category = ProcessCategory.STORAGE
        aquifer.section = OverviewSelection.WATER
        aquifer.variables = List([
            PropertyVariable("Content", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Shunt", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Influx", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS)
        ])
        aquifer.properties = List([
            PropertyLineEdit("Catchment Area", "2", "km2"),
            PropertyLineEdit("Aquifer Height", "0.8", "m")
        ])
        aquifer.inputs = List([
            Commodity("Groundwater", commodity_types[4], DatasetResolution.HOURLY)
        ])
        aquifer.outputs = List([
            Commodity("Groundwater", commodity_types[4], DatasetResolution.HOURLY)
        ])
        aquifer.objective_function = "influx * 1000"
        aquifer.constraints = """
        content == content[-1] + groundwater_in - groundwater_out + influx - shunt
        content <= aquifer_height * catchment_area * 1000000"""

        maize_field = ProcessCore()
        maize_field.name = "Maize Field"
        maize_field.icon = QIcon(QPixmap(":/icons/img/maize_field@2x.png"))
        maize_field.category = ProcessCategory.PROCESS
        maize_field.section = OverviewSelection.FOOD
        maize_field.variables = List([
            PropertyVariable("Evaporation Canopy", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Evaporation Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Evaporation Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number 1", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number 3", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Runoff", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Capacity Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Capacity Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Content Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Topsoil Overflow", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("Content Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("w1", DatasetResolution.DAILY, PyomoVarType.BOOLEAN),
            PropertyVariable("w2", DatasetResolution.DAILY, PyomoVarType.BOOLEAN),
            PropertyVariable("w3", DatasetResolution.DAILY, PyomoVarType.BOOLEAN),
            PropertyVariable("x1", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("x2", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("x3", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("y1", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("y2", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS),
            PropertyVariable("y3", DatasetResolution.DAILY, PyomoVarType.NON_NEGATIVE_REALS)
        ])
        maize_field.data = List([
            PropertyValue("WACC", "0.15"),
            PropertyValue("Curve Number 2", "85"),
            PropertyValue("Evaporation Topsoil Percentage", "1"),
            PropertyValue("Evaporation Middlesoil Percentage", "0.75"),
            PropertyValue("Biomass", "20000", "kg/ha"),
            PropertyValue("LAI max", "6.1"),
            PropertyValue("Canopy max", "4", "mm"),
            PropertyValue("Field Capacity", "0.32"),
            PropertyValue("Wilting Point", "0.15"),
            PropertyValue("Topsoil Thickness", "400", "mm"),
            PropertyValue("Seed Amount", "25", "kg/ha"),
            PropertyValue("Compound D Amount", "165", "kg/ha"),
            PropertyValue("Top Dressing Amount", "200", "kg/ha"),
            PropertyValue("Pesticides Amount", "200", "kg/ha"),
            PropertyValue("Labor Amount", "814", "h/ha"),
            PropertyValue("Maize Yield", "8000", "kg/ha"),
            PropertyValue("Maize Straw Yield", "8000", "kg/ha"),
        ])
        maize_field.properties = List([
            PropertyPopupMenu("Precipitation", time_series),
            PropertyPopupMenu("Evapotranspiration", time_series),
            PropertyPopupMenu("Leaf Area Index", time_series),
            PropertyPopupMenu("k_c", time_series),
            PropertyPopupMenu("Harvest Series", time_series),
            PropertyLineEdit("Life Time", "50", "a"),
            PropertyLineEdit("Irrigation System Investment", "2000", "$/ha"),
            PropertyLineEdit("Irrigation System Fixed Costs", "40", "$/ha"),
            PropertyLineEdit("Seed Price", "2.3", "$/kg"),
            PropertyLineEdit("Compound D Price", "1.04", "$/kg"),
            PropertyLineEdit("Top Dressing Price", "5.08", "$/kg"),
            PropertyLineEdit("Pesticides Price", "1.41", "$/kg"),
            PropertyLineEdit("Labor Price", "1.25", "$/h")
        ])
        maize_field.inputs = List([
            Commodity("Crop Land", commodity_types[6], DatasetResolution.YEARLY),
            Commodity("Water", commodity_types[4], DatasetResolution.DAILY)
        ])
        maize_field.outputs = List([
            Commodity("Groundwater", commodity_types[4], DatasetResolution.DAILY),
            Commodity("Maize", commodity_types[5], DatasetResolution.WEEKLY),
            Commodity("Maize Straw", commodity_types[3], DatasetResolution.WEEKLY)
        ])
        maize_field.objective_function = """crop_land * (irrigation_system_investment * ((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc)
         + irrigation_system_fixed_costs) 
        ++ (seed_price*seed_amount + compound_d_price*compound_d_amount + top_dressing_price*top_dressing_amount + 
        pesticides_price*pesticides_amount + labor_price*labor_amount)/maize_yield*maize*168 ++ content_middlesoil*10"""
        maize_field.constraints = """
        evaporation_canopy = min(precipitation, leaf_area_index/lai_max * canopy_max, evapotranspiration)
        evaporation_topsoil = (evapotranspiration - evaporation_canopy)*evaporation_topsoil_percentage*exp(-5*10**(-5)*biomass)
        evaporation_middlesoil = max(0, (evapotranspiration - evaporation_canopy-evaporation_topsoil)*evaporation_topsoil_percentage* exp(-5*10**(-5)*biomass))
        capacity_topsoil = (field_capacity-wilting_point)*topsoil_thickness
        capacity_middlesoil = (field_capacity-wilting_point-0.1)*(500 - topsoil_thickness)
        curve_number_1 = curve_number_2 - 20*(100-curve_number_2)/(100-curve_number_2+exp(2.533-0.0636*(100-curve_number_2)))
        curve_number_3 = curve_number_2*exp(0.00673*(100-curve_number_2))
        curve_number = curve_number_3 if (precipitation-evaporation_canopy > capacity_topsoil) else (curve_number_1 if (precipitation-evaporation_canopy < 0.001) else curve_number_2)
        runoff = min(precipitation-evaporation_canopy, (precipitation-evaporation_canopy-0.2*25.4*(1000/curve_number-10))**2/(precipitation-evaporation_canopy+0.5*25.4*(1000/curve_number_2-10)))
        content_topsoil[-1] + water + (precipitation - evaporation_canopy - runoff - evaporation_topsoil - evapotranspiration * k_c) * crop_land * 10/24 == x1 + y1 + topsoil_overflow
        content_topsoil == x1 + y1
        x1 <= capacity_topsoil*crop_land*10/24 - y1
        topsoil_overflow <= w1*48*10/24*100
        topsoil_overflow <= crop_land*10/24*max(0, precipitation - evaporation_canopy - runoff - evaporation_topsoil - evapotranspiration * k_c)
        y1 <= w1*capacity_topsoil*100*10/24
        y1 <= capacity_topsoil*crop_land*10/24
        y1 >= capacity_topsoil*crop_land*10/24 - (1-w1)*capacity_topsoil*100*10/24
        content_middlesoil[-1] + topsoil_overflow - evaporation_middlesoil * crop_land*10/24 == x2 + y2 - x3 + groundwater
        content_middlesoil == x2 + y2
        x2 <= capacity_middlesoil*crop_land*10/24 - y2 - y3
        x3 <= evaporation_middlesoil*10/24*100*w3
        x3 <= evaporation_middlesoil*crop_land*10/24 
        w2 + w3 <= 1
        groundwater <= w2*48*10/24*100
        groundwater <= crop_land*10/24*max(0, precipitation - evaporation_canopy - runoff - evaporation_topsoil - evapotranspiration * k_c)
        y2 <= w2*capacity_middlesoil*100*10/24
        y2 <= capacity_middlesoil*crop_land*10/24
        y2 >= capacity_middlesoil*crop_land*10/24 - (1-w2)*capacity_middlesoil*100*10/24
        y3 <= w3*evaporation_middlesoil*100*10/24
        y3 <= evaporation_middlesoil*crop_land*10/24
        y3 >= evaporation_middlesoil*crop_land*10/24 - (1-w3)*evaporation_middlesoil*100*10/24
        maize_straw == harvest_series * crop_land * maize_straw_yield / 168
        maize == harvest_series * crop_land * maize_yield / 168"""

        land_distribution = ProcessCore()
        land_distribution.name = "Land Distribution"
        land_distribution.icon = QIcon(QPixmap(":/icons/img/land_size@2x.png"))
        land_distribution.category = ProcessCategory.SUPPLY
        land_distribution.section = OverviewSelection.FOOD
        land_distribution.properties = List([
            PropertyLineEdit("Total Land Size", "100", "ha"),
            PropertyLineEdit("Fallow Land Restriction", "100", "ha"),
            PropertyLineEdit("Forest Land Restriction", "100", "ha"),
            PropertyLineEdit("Crop Land Restriction", "100", "ha"),
        ])
        land_distribution.outputs = List([
            Commodity("Fallow Land", commodity_types[6], DatasetResolution.YEARLY),
            Commodity("Forest Land", commodity_types[6], DatasetResolution.YEARLY),
            Commodity("Crop Land", commodity_types[6], DatasetResolution.YEARLY)
        ])
        land_distribution.objective_function = ""
        land_distribution.constraints = """fallow_land <= fallow_land_restriction
        crop_land <= crop_land_restriction
        forest_land <= forest_land_restriction
        total_land_size == fallow_land + crop_land + forest_land"""

        maize_straw_bunker = ProcessCore()
        maize_straw_bunker.name = "Maize Straw Silo"
        maize_straw_bunker.icon = QIcon(QPixmap(":/icons/img/maize_straw_silo@2x.png"))
        maize_straw_bunker.category = ProcessCategory.STORAGE
        maize_straw_bunker.section = OverviewSelection.FOOD
        maize_straw_bunker.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS),
            PropertyVariable("Content", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS)
        ])
        maize_straw_bunker.data = List([
            PropertyValue("WACC", "0.15")
        ])
        maize_straw_bunker.properties = List([
            PropertyLineEdit("Size", "5", "t"),
            PropertyLineEdit("Life Time", "50", "a"),
            PropertyLineEdit("Investment Cost", "100", "$/kg")
        ])
        maize_straw_bunker.inputs = List([
            Commodity("Maize Straw", commodity_types[3], DatasetResolution.HOURLY)
        ])
        maize_straw_bunker.outputs = List([
            Commodity("Maize Straw", commodity_types[3], DatasetResolution.HOURLY)
        ])
        maize_straw_bunker.objective_function = "size*amount*investment_cost * " \
                                                "((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc)"
        maize_straw_bunker.constraints = """content == content[-1] + maize_straw_in - maize_straw_out
        content <= size*amount*1000"""

        water_tank = ProcessCore()
        water_tank.name = "Water Tank"
        water_tank.icon = QIcon(QPixmap(":/icons/img/water_tank@2x.png"))
        water_tank.category = ProcessCategory.STORAGE
        water_tank.section = OverviewSelection.WATER
        water_tank.variables = List([
            PropertyVariable("Amount", DatasetResolution.YEARLY, PyomoVarType.NON_NEGATIVE_INTEGERS),
            PropertyVariable("Content", DatasetResolution.HOURLY, PyomoVarType.NON_NEGATIVE_REALS)
        ])
        water_tank.data = List([
            PropertyValue("WACC", "0.15")
        ])
        water_tank.properties = List([
            PropertyLineEdit("Size", "20", "m3"),
            PropertyLineEdit("Life Time", "25", "a"),
            PropertyLineEdit("Investment Cost", "35", "$/m3"),
            PropertyLineEdit("Fixed Cost", "0.35", "$/m3")
        ])
        water_tank.inputs = List([
            Commodity("Water", commodity_types[4], DatasetResolution.HOURLY)
        ])
        water_tank.outputs = List([
            Commodity("Water", commodity_types[4], DatasetResolution.HOURLY)
        ])
        water_tank.objective_function = "size*amount*(investment_cost * " \
                                        "((1+wacc)**life_time-1)/((1+wacc)**life_time*wacc) + fixed_cost)"
        water_tank.constraints = """content == content[-1] + water_in - water_out
                content <= size*amount*1000"""

        forest_land = ProcessCore()
        forest_land.name = "Forest Land"
        forest_land.icon = QIcon(QPixmap(":/icons/img/forest_land@2x.png"))
        forest_land.category = ProcessCategory.SUPPLY
        forest_land.section = OverviewSelection.WATER
        forest_land.variables = List([
            PropertyVariable("Evaporation Canopy", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Evaporation Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Evaporation Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number 1", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number 3", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Runoff", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Capacity Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Capacity Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Content Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Topsoil Overflow", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Content Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO)
        ])
        forest_land.data = List([
            PropertyValue("WACC", "0.15"),
            PropertyValue("Curve Number 2", "79"),
            PropertyValue("Evaporation Topsoil Percentage", "1"),
            PropertyValue("Evaporation Middlesoil Percentage", "0.75"),
            PropertyValue("Biomass", "80000", "kg/ha"),
            PropertyValue("LAI max", "2.5"),
            PropertyValue("Canopy max", "3.5", "mm"),
            PropertyValue("Field Capacity", "0.32"),
            PropertyValue("Wilting Point", "0.15"),
            PropertyValue("Topsoil Thickness", "200", "mm")
        ])
        forest_land.properties = List([
            PropertyPopupMenu("Precipitation", time_series),
            PropertyPopupMenu("Evapotranspiration", time_series),
            PropertyPopupMenu("Leaf Area Index", time_series)
        ])
        forest_land.inputs = List([
            Commodity("Forest Land", commodity_types[6], DatasetResolution.YEARLY)
        ])
        forest_land.outputs = List([
            Commodity("Groundwater", commodity_types[4], DatasetResolution.DAILY)
        ])
        forest_land.constraints = """
                evaporation_canopy = min(precipitation, leaf_area_index/lai_max * canopy_max, evapotranspiration)
                evaporation_topsoil = (evapotranspiration - evaporation_canopy)*evaporation_topsoil_percentage*exp(-5*10**(-5)*biomass)
                evaporation_middlesoil = max(0, (evapotranspiration - evaporation_canopy-evaporation_topsoil)*evaporation_topsoil_percentage* exp(-5*10**(-5)*biomass))
                capacity_topsoil = (field_capacity-wilting_point)*topsoil_thickness
                capacity_middlesoil = (field_capacity-wilting_point-0.1)*(500 - topsoil_thickness)
                curve_number_1 = curve_number_2 - 20*(100-curve_number_2)/(100-curve_number_2+exp(2.533-0.0636*(100-curve_number_2)))
                curve_number_3 = curve_number_2*exp(0.00673*(100-curve_number_2))
                curve_number = curve_number_3 if (precipitation-evaporation_canopy > capacity_topsoil) else (curve_number_1 if (precipitation-evaporation_canopy < 0.001) else curve_number_2)
                runoff = min(precipitation-evaporation_canopy, (precipitation-evaporation_canopy-0.2*25.4*(1000/curve_number-10))**2/(precipitation-evaporation_canopy+0.5*25.4*(1000/curve_number_2-10)))
                content_topsoil = min((content_topsoil[-1] if content_topsoil[-1] else 0.2*capacity_topsoil) + precipitation - evaporation_canopy - runoff - evaporation_topsoil - transpiration_plant, capacity_topsoil)
                topsoil_overflow = max(0, (content_topsoil[-1] if content_topsoil[-1] else 0.2*capacity_topsoil) + precipitation - evaporation_canopy - runoff - evaporation_topsoil - transpiration_plant - capacity_topsoil)
                content_middlesoil = min((content_middlesoil[-1] if content_middlesoil[-1] else 0.2*capacity_middlesoil) + topsoil_overflow - evaporation_middlesoil, capacity_middlesoil)
                groundwater == forest_land * 10/24 * max(0, (content_middlesoil[-1] if content_middlesoil[-1] else 0.2*capacity_middlesoil) + topsoil_overflow - evaporation_middlesoil - capacity_middlesoil)"""

        fallow_land = ProcessCore()
        fallow_land.name = "Fallow Land"
        fallow_land.icon = QIcon(QPixmap(":/icons/img/fallow_land@2x.png"))
        fallow_land.category = ProcessCategory.SUPPLY
        fallow_land.section = OverviewSelection.WATER
        fallow_land.variables = List([
            PropertyVariable("Evaporation Canopy", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Evaporation Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Evaporation Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number 1", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Curve Number 3", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Runoff", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Capacity Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Capacity Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Content Topsoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Topsoil Overflow", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO),
            PropertyVariable("Content Middlesoil", DatasetResolution.DAILY, PyomoVarType.NON_PYOMO)
        ])
        fallow_land.data = List([
            PropertyValue("WACC", "0.15"),
            PropertyValue("Curve Number 2", "93"),
            PropertyValue("Evaporation Topsoil Percentage", "1"),
            PropertyValue("Evaporation Middlesoil Percentage", "0.75"),
            PropertyValue("Biomass", "30", "kg/ha"),
            PropertyValue("LAI max", "0.2"),
            PropertyValue("Canopy max", "0.2", "mm"),
            PropertyValue("Field Capacity", "0.32"),
            PropertyValue("Wilting Point", "0.15"),
            PropertyValue("Topsoil Thickness", "50", "mm")
        ])
        fallow_land.properties = List([
            PropertyPopupMenu("Precipitation", time_series),
            PropertyPopupMenu("Evapotranspiration", time_series),
            PropertyPopupMenu("Leaf Area Index", time_series)
        ])
        fallow_land.inputs = List([
            Commodity("Fallow Land", commodity_types[6], DatasetResolution.YEARLY)
        ])
        fallow_land.outputs = List([
            Commodity("Groundwater", commodity_types[4], DatasetResolution.DAILY)
        ])
        fallow_land.constraints = """
                evaporation_canopy = min(precipitation, leaf_area_index/lai_max * canopy_max, evapotranspiration)
                evaporation_topsoil = (evapotranspiration - evaporation_canopy)*evaporation_topsoil_percentage*exp(-5*10**(-5)*biomass)
                evaporation_middlesoil = max(0, (evapotranspiration - evaporation_canopy-evaporation_topsoil)*evaporation_topsoil_percentage* exp(-5*10**(-5)*biomass))
                capacity_topsoil = (field_capacity-wilting_point)*topsoil_thickness
                capacity_middlesoil = (field_capacity-wilting_point-0.1)*(500 - topsoil_thickness)
                curve_number_1 = curve_number_2 - 20*(100-curve_number_2)/(100-curve_number_2+exp(2.533-0.0636*(100-curve_number_2)))
                curve_number_3 = curve_number_2*exp(0.00673*(100-curve_number_2))
                curve_number = curve_number_3 if (precipitation-evaporation_canopy > capacity_topsoil) else (curve_number_1 if (precipitation-evaporation_canopy < 0.001) else curve_number_2)
                runoff = min(precipitation-evaporation_canopy, (precipitation-evaporation_canopy-0.2*25.4*(1000/curve_number-10))**2/(precipitation-evaporation_canopy+0.5*25.4*(1000/curve_number_2-10)))
                content_topsoil = min((content_topsoil[-1] if content_topsoil[-1] else 0.2*capacity_topsoil) + precipitation - evaporation_canopy - runoff - evaporation_topsoil - transpiration_plant, capacity_topsoil)
                topsoil_overflow = max(0, (content_topsoil[-1] if content_topsoil[-1] else 0.2*capacity_topsoil) + precipitation - evaporation_canopy - runoff - evaporation_topsoil - transpiration_plant - capacity_topsoil)
                content_middlesoil = min((content_middlesoil[-1] if content_middlesoil[-1] else 0.2*capacity_middlesoil) + topsoil_overflow - evaporation_middlesoil, capacity_middlesoil)
                groundwater == fallow_land * 10/24 * max(0, (content_middlesoil[-1] if content_middlesoil[-1] else 0.2*capacity_middlesoil) + topsoil_overflow - evaporation_middlesoil - capacity_middlesoil)"""

        return List([pv_core, diesel_core, digester_core, diesel_market_core, biowaste_market_core, battery_core,
                     biogas_tank_core, biogas_gen_core, electrical_demand_core, village_water_demand, water_pump,
                     aquifer, maize_field, land_distribution, food_market, maize_straw_bunker, forest_land, fallow_land,
                     water_tank])

    @staticmethod
    def time_series():
        return List([])

    @staticmethod
    def commodities():
        return List([
            CommodityType("Energy"),
            CommodityType("Fuel"),
            CommodityType("Biogas"),
            CommodityType("Biowaste"),
            CommodityType("Water"),
            CommodityType("Food"),
            CommodityType("Land")
        ])
