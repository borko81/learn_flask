from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

memory_data = {"person_info": [{"name": "person_one", "age": 40}, {"name": "person two", "age": 39}]}


class Persons(Resource):
    def get(self):
        return jsonify(memory_data)

    def post(self):
        data = request.get_json()
        name: str = data['name']
        age: int = data['age']
        try:
            _ = [result['name'] for result in memory_data["person_info"] if result["name"] == name][0]
            return {"message": "This name is already in collection"}, 400
        except IndexError:
            memory_data['person_info'].append({"name": name, "age": age})
            return {"message": "Success"}, 201


class PersonFromName(Resource):
    def get(self, name):
        try:
            data = [item for item in memory_data['person_info'] if item['name'] == name][0]
            return jsonify(data)
        except IndexError:
            return {"message": "Exit with error"}, 400


api.add_resource(Persons, "/persons")
api.add_resource(PersonFromName, '/person/<name>')

if __name__ == '__main__':
    app.run()
