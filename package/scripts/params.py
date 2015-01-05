#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *

# server configurations
config = Script.get_config()

install_eclipse = config['configurations']['vnc-config']['install.eclipse']
vnc_password = config['configurations']['vnc-config']['vnc.password']
vnc_geometry = config['configurations']['vnc-config']['vnc.geometry']

