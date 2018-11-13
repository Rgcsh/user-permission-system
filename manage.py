from flask_script import Manager

from ups import create_app, db

app = create_app('dev')
with app.app_context():
    db.create_all()

manager = Manager(app)


@manager.option('-p', '--port', help='Server run port', default=5000)
@manager.option('-h', '--host', help='Server run host', default='0.0.0.0')
@manager.option('-t', '--thread', help='Thread count', default=2)
def start(host, port, thread):
    app.run(host=host, port=int(port), processes=int(thread),thread=True)


if __name__ == '__main__':
    manager.run()
