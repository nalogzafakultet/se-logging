from project import db

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service = db.Column(db.String(128), nullable=False)
    endpoint = db.Column(db.String(128), nullable=False)
    visitor_ip = db.Column(db.String(128), nullable=False)
    visit_time = db.Column(db.DateTime, nullable=False)


    def __init__(self, service, endpoint, visitor_ip, visit_time):
        self.service = service
        self.endpoint = endpoint
        self.visitor_ip = visitor_ip
        self.visit_time = visit_time

    def to_json(self):
        return {
            'service': self.service,
            'endpoint': self.endpoint,
            'visitor_ip': self.visitor_ip,
            'visit_time': self.visit_time
        }