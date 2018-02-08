from project import db

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(128), nullable=False)

    def __init__(self, path):
        self.path = path

    def to_json(self):
        return {
        'id': self.id,
        'path': self.path,
    }