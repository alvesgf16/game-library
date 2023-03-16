from flaskr import db


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name
