#!/bin/bash

source venv/bin/activate

#
# Execution Phase
#

python run_admin.py $@

#
# Breakdown Phase
#

deactivate
