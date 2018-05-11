from metaswitch_tinder.global_config import DATABASE as db

class User(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


def list_all_users():
    return User.query.all()

#db.create_all()
#User.__table__.create(db.session.bind)

#X = User("James", "james.jameson@metaswitch.com")
#db.session.add(X)
#db.session.commit()
