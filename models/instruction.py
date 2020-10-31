from extensions import db
# This is /models/instruction.py designed to meet the needs for practical ex. 2
instruction_list = []

# This is the database model for SQLAlchemy, it has variables for all the columns we need


class Instruction(db.Model):

    __tablename__ = 'instruction'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    tools = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    steps = db.Column(db.String(1000))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))


    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tools': self.tools,
            'duration': self.duration,
            'steps': self.steps,
            'user_id': self.user_id
        }


    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()


    @classmethod
    def get_by_id(cls, instruction_id):
        return cls.query.filter_by(id=Instruction.id).first()


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()