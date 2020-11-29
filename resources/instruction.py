from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

from models.instruction import Instruction

# This is the resources/instruction.py for web app. It is kinda similiar from the earlier projects, so I kinda reused it
# Works fine as always.

from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.instruction import Instruction
from schemas.instruction import InstructionSchema

instruction_schema = InstructionSchema()
instruction_list_schema = InstructionSchema(many=True)


class InstructionListResource(Resource):

    def get(self):

        instructions = Instruction.get_all_published()

        return instruction_list_schema.dump(instructions).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = instruction_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        recipe = Instruction(**data)
        recipe.user_id = current_user
        recipe.save()

        return instruction_schema.dump(recipe).data, HTTPStatus.CREATED


class InstructionResource(Resource):

    @jwt_optional
    def get(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if instruction.is_publish == False and instruction.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return instruction.data(), HTTPStatus.OK

    @jwt_required
    def put(self, instruction_id):

        json_data = request.get_json()

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.name = json_data['name']
        instruction.description = json_data['description']
        instruction.tools = json_data['tools']
        instruction.duration = json_data['duration']
        instruction.steps = json_data['steps']

        instruction.save()

        return instruction.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.delete()

        return {}, HTTPStatus.NO_CONTENT


class InstructionPublishResource(Resource):

    @jwt_required
    def put(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.is_publish = True
        instruction.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.is_publish = False
        instruction.save()

        return {}, HTTPStatus.NO_CONTENT








#This is the old stuff for chapter 4...
"""
class InstructionListResource(Resource):

    def get(self):

        instructions = Instruction.get_all_published()

        data = []

        for instruction in instructions:
            data.append(instruction.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required

    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()

        instruction = Instruction(name=json_data['name'],
                        description=json_data['description'],
                        tools=json_data['tools'],
                        duration=json_data['duration'],
                        steps=json_data['steps'],
                        user_id=current_user)

        instruction.save()

        return instruction.data(), HTTPStatus.CREATED


class InstructionResource(Resource):

    @jwt_optional

    def get(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=Instruction.id)

        if instruction is None:
            return {'message': 'Instruction not found :/'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if instruction.is_publish == False and instruction.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return instruction.data(), HTTPStatus.OK

    @jwt_required
    def put(self, instruction_id):

        json_data = request.get_json()

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found! :('}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.name = json_data['name']
        instruction.description = json_data['description']
        instruction.tools = json_data['tools']
        instruction.duration = json_data['duration']
        instruction.steps = json_data['steps']

        instruction.save()

        return instruction.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found... :('}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.delete()

        return {}, HTTPStatus.NO_CONTENT



class InstructionPublishResource(Resource):

    @jwt_required
    def put(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.is_publish = True
        instruction.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.is_publish = False
        instruction.save()

        return {}, HTTPStatus.NO_CONTENT
"""
