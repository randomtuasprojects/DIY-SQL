# This is that app.py for practical ex. 2. Runs smoothly on flask.

from flask import Flask
from flask_restful import Api

from resources.instruction import InstructionListResource, InstructionResource, InstructionPublishResource

app = Flask(__name__)
api = Api(app)

api.add_resource(InstructionListResource, '/instructions')
api.add_resource(InstructionResource, '/instructions/<int:instruction_id>')
api.add_resource(InstructionPublishResource, '/instructions/<int:instruction_id>/publish')

if __name__ == '__main__':
    app.run(port=5000, debug=True)