#!/usr/bin/env python
from resource_management import *

# server configurations
config = Script.get_config()

template_config = config['configurations']['vnc-env']['content']