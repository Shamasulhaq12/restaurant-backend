import os
import sys

# Path to the project directory
project_home = '/home/bookcgtu/server-test'

# Add the project directory to the sys.path
if project_home not in sys.path:
    sys.path.append(project_home)

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'coresite.settings'

# Load the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



