from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

memory_data = {"person_info": [{"name": "person_one", "age": 40}, {"name": "person two", "age": 39}]}

def validate_name_exists(memory, name):
    return [item for item in memory['person_info'] if item['name'] == name][0]

class Persons(Resource):
    def get(self):
        return jsonify(memory_data)

    def post(self):
        data = request.get_json()
        name: str = data['name']
        age: int = data['age']
        try:
            _ = validate_name_exists(memory_data, name)
            return {"message": "This name is already in collection"}, 400
        except IndexError:
            memory_data['person_info'].append({"name": name, "age": age})
            return {"message": "Success"}, 201


class PersonFromName(Resource):
    def get(self, name):
        try:
            data = validate_name_exists(memory_data, name)
            return jsonify(data)
        except IndexError:
            return {"message": "Exit with error"}, 400

    def delete(self, name):
        try:
            _ = validate_name_exists(memory_data, name)
            memory_data['person_info'] = [found_name for found_name in memory_data['person_info'] if not found_name['name'] == name]
            return {"message": "Successfully delete"}, 204
        except IndexError:
            return {"message": "Exit with error"}, 400

    def put(self, name):
        data = request.get_json()
        new_name = data['new_name']
        new_age = data['new_age']
        try:
            found = validate_name_exists(memory_data, name)
            found['name'] = new_name
            found['age'] = new_age
            return {"message": "Success"}, 200
        except IndexError:
            return {"message": "Exit with error"}, 400



api.add_resource(Persons, "/persons")
api.add_resource(PersonFromName, '/person/<name>')

if __name__ == '__main__':
    app.run()
