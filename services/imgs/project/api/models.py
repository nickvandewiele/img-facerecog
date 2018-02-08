from project import db

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.Text(), nullable=False)
    names = db.Column(db.Text(), nullable=True)

    def __init__(self, path, names=None):
        self.path = path
        self.names = names

    def to_json(self):
        return {
        'id': self.id,
        'path': self.path,
        'names': self.names,
    }