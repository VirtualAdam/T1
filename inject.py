from datetime import datetime
from app import db, create_app
from app.models import User, Post
from flask_login import current_user, login_user

def posit(message,name,photo):
	app = create_app()
	app.app_context().push()
	u = User.query.filter_by(username=name).first()
	print u
	p = Post(body=message, author=u, photo_id=photo)
	db.session.add(p)
	db.session.commit()


