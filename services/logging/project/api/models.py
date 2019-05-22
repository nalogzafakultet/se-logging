from project import db

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service = db.Column(db.String(128), nullable=False)
    endpoint = db.Column(db.String(128), nullable=False)

    def __init__(self, service, endpoint):
        self.service = service
        self.endpoint = endpoint

    def to_json(self):
        return {
            'service': self.service,
            'endpoint': self.endpoint
        }