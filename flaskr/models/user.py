from flaskr import db


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def password_matches(self, a_password: str) -> bool:
        assert isinstance(self.password, str)
        return a_password == self.password

    def __repr__(self) -> str:
        return '<Name %r>' % self.name
