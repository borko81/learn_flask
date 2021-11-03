import json
import unittest
from app import memory_data, app, Persons
from copy import deepcopy


class TestPerson(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/persons'

    def setUp(self):
        self.data = deepcopy(memory_data)
        self.client = app.test_client()

    def test_return_persons(self):
        response = self.client.get(TestPerson.URL)
        self.assertEqual(response.status_code, 200)

    def test_post_persons_when_person_exists(self):
        item = {"name": "person two", "age": 40}
        before_send = len(memory_data['person_info'])
        response = self.client.post(
            TestPerson.URL,
            data=json.dumps(item),
            content_type="application/json"
        )
        self.assertEqual(before_send, len(memory_data['person_info']))
        self.assertEqual(400, response.status_code)

    def test_post_person_whith_corect_new_name(self):
        item = {"name": "Borko", "age": 40}
        before_send = len(memory_data['person_info'])
        response = self.client.post(
            TestPerson.URL,
            data=json.dumps(item),
            content_type="application/json"
        )
        self.assertEqual(201, response.status_code)
        print(before_send)

    def tearDown(self) -> None:
        memory_data = self.data


if __name__ == '__main__':
    unittest.main()
