# globals.py
# Define global constants

from django.conf import settings

NS2_PATH = '/usr/local/bin/ns'
BASH_PATH = '/bin/bash'

if settings.__ENV_PROD__:
    # Prod
    NS2_SCRIPT_STORAGE_PATH = '/var/ns2web'
else:
    # Dev
    NS2_SCRIPT_STORAGE_PATH = '/var/ns2web_demo'
