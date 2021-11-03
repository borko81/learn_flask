from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

memory_data = {"person_info": [{"name": "person one", "age": 40}, {"name": "person two", "age": 39}]}


class Persons(Resource):
    def get(self):
        return jsonify(memory_data)

    def post(self):
        data = request.get_json()
        name = data['name']
        age = data['age']
        try:
            _ = [name for result in memory_data["person_info"] if result["name"] == name][0]
            return {"message": "This name is already in collection"}, 400
        except IndexError:
            memory_data['person_info'].append({"name": name, "age": age})
            return jsonify(memory_data)


api.add_resource(Persons, "/persons")

if __name__ == '__main__':
    app.run()
