from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from app import create_app, db
from app.models import *

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,UserLog=UserLog,UserOpLog=UserLog,Tag=Tag,Comment=Comment,Resource=Resource,ResourceCol=ResourceCol,followers=followers,Auth=Auth,Role=Role,Admin=Admin,AdminLog=AdminLog,AdminOpLog=AdminOpLog)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()