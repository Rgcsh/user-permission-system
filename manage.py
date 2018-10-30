from ups import create_app, db

app = create_app('dev')
with app.app_context():
	db.create_all()

if __name__ == '__main__':
	app.run()
