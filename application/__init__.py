from factory import create_app
from flask.ext.sqlalchemy import SQLAlchemy

app = create_app()

app.template_folder = 'application/templates'
app.static_folder = 'application/static'

class UnLockedAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        if not "isolation_level" in options:
            options["isolation_level"] = "READ COMMITTED" 
        return super(UnLockedAlchemy, self).apply_driver_hacks(app, info, options)

db = UnLockedAlchemy(app)

import tasks
from models import *