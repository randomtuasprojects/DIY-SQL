# This is the instruction.py for practical ex. 1

from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

# Here be the instructions in JSON. reformattted by me. Lets just leave this here for now

instructions = [
    {
    "id": 1,
    "name": "Paint a wall",
    "description": "Instructions how to paint a wall",
    "steps": [" Clean the wall", "Tape the trim",
        "Roll the primer onto the wall",
        "Paint the trim", "Remove the painter's tape"],
    "tools": ["painter's tape", "primer", "paint", "paint roller",
        "paint tray", " paintbrush"],
    "cost": 100,
    "duration": 8
    },
    {
    "id": 2,
    "name": "Clean Windows",
    "description": "Instructions how to wash windows",
    "steps": ["Mix soap with water", "Add 1/1000th part of Vinegar", "Apply to window surface with a sponge",
        "Remove excess mixture with a spatula", "Repeat if necessary"],
    "tools": ["Bucket", "Sponge", "Spatula"],
    "cost": 15,
    "duration": 1
    }
]



# HTTP verbs start here
# GET all
@app.route('/instructions', methods=['GET'])
def get_instructions():
    return jsonify({'data': instructions})

# GET one specific by instruction ID

@app.route('/instructions/<int:instruction_id>', methods=['GET'])
def get_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction["id"] == instruction_id), None)

    if instruction:
        return jsonify(instruction)

    return jsonify({'message': 'instruction not found'}), HTTPStatus.NOT_FOUND

# POST / Create new

@app.route('/instructions', methods=['POST'])
def create_instructions():
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")

    instruction = {
        "id": len(instructions) + 1,
        "name": name,
        "description": description
    }

    instructions.append(instruction)

    return jsonify(instruction), HTTPStatus.CREATED

# PUT / Update

@app.route('/instructions/<int:instruction_id>', methods=['PUT'])
def update_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)

    if not instruction:
        return jsonify({'message': 'instruction not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    instruction.update(
        {
            'name': data.get("name"),
            'description': data.get("description")
        }
    )

    return jsonify(instruction)

# DELETE instruction
@app.route('/instructions/<int:instruction_id>', methods=['DELETE'])

def delete_instruction(instruction_id):

    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)

    if not instruction:

        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    instructions.remove(instruction)

    return '', HTTPStatus.NO_CONTENT

if __name__ == '__main__':
    app.run()