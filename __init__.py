import os
import settings

if settings.__ENV_PROD__:
	os.environ['MPLCONFIGDIR'] = '/var/ns2web/matplotlib'
