import json
import unittest
import app
from copy import deepcopy


class TestSpecificPerson(unittest.TestCase):
    URL = "http://127.0.0.1:5000/person"

    def setUp(self) -> None:
        self.client = app.app.test_client()
        self.backup = deepcopy(app.memory_data)

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

    def test_delete_person_when_his_name_exists_return_204(self):
        name = "person_one"
        before_del = len(app.memory_data['person_info'])
        response = self.client.delete(
            TestSpecificPerson.URL + "/" + name,
            content_type = "application/json"
        )
        after_del = len(app.memory_data['person_info'])
        self.assertNotEqual(before_del, after_del)
        self.assertEqual(204, response.status_code)

    def test_delete_when_name_not_in_data_should_return_status_400(self):
        name = "person_one1"
        before_del = len(app.memory_data['person_info'])
        response = self.client.delete(
            TestSpecificPerson.URL + "/" + name,
            content_type="application/json"
        )
        after_del = len(app.memory_data['person_info'])
        self.assertEqual(before_del, after_del)
        self.assertEqual(400, response.status_code)

    def test_put_new_data_when_found_name_in_memory_changeit(self):
        name = 'person_one'
        data = {'new_name': "test", "new_age": 41}
        response = self.client.put(
            TestSpecificPerson.URL + "/" + name,
            data = json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("Success", json.loads(response.data)['message'])
        print(app.memory_data['person_info'])


    def tearDown(self) -> None:
        app.memory_data = self.backup


if __name__ == '__main__':
    unittest.main()
