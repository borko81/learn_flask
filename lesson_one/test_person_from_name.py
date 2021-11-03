import json
import unittest
from app import memory_data, app
from copy import deepcopy


class TestSpecificPerson(unittest.TestCase):
    URL = "http://127.0.0.1:5000/person"

    def setUp(self) -> None:
        self.client = app.test_client()
        self.backup = deepcopy(memory_data)

    def test_return_person_from_name_when_name_exists(self):
        name = 'person_one'
        response = self.client.get(
            TestSpecificPerson.URL + "/" + name,
            content_type="application/json"
        )
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(40, data['age'])

    def test_get_concret_person_when_not_exists_should_return_400(self):
        name = 'borko'
        response = self.client.get(
            TestSpecificPerson.URL + "/" + name,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual("Exit with error", result['message'])

    def tearDown(self) -> None:
        memory_data = self.backup


if __name__ == '__main__':
    unittest.main()
