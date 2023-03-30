from flask_bcrypt import check_password_hash, generate_password_hash

from flaskr import db


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def password_matches(self, a_password: str) -> bool:
        return check_password_hash(self.password_hash, a_password)

    def set_password(self, a_password):
        self.password_hash = generate_password_hash(a_password)

    password = property(fset=set_password)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name
