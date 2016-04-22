import os

# Production settings
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    # If we are in prod, load prod configs
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root@/physical_web?unix_socket=/cloudsql/stoked-archway-837:gamenight-backend-central"
    DEBUG = False
    
# Dev settings
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tmp/test.db'
    DEBUG = True

# General settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
