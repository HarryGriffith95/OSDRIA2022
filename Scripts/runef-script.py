
# -*- coding: utf-8 -*-
import re
import sys

from pyomo.pysp.ef_writer_script import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())