from factory import create_app
from flask.ext.sqlalchemy import SQLAlchemy

application = create_app()

application.template_folder = 'app/templates'
application.static_folder = 'app/static'

class UnLockedAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        if not "isolation_level" in options:
            options["isolation_level"] = "READ COMMITTED" 
        return super(UnLockedAlchemy, self).apply_driver_hacks(app, info, options)

db = UnLockedAlchemy(application)

import tasks
from models import *