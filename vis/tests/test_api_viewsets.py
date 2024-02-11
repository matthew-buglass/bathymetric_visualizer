import json

import numpy as np
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APIRequestFactory

from vis.api_viewsets import add_point_to_mesh
from vis.models import ThreeDimensionalMesh


# Using the standard RequestFactory API to create a form POST request
# factory = APIRequestFactory()
# request = factory.post('/notes/', {'title': 'new idea'})


class TestAddPointToMesh(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.request_factory = APIRequestFactory()
        cls.endpoint = "/api/mesh/add_point/"
        cls.x = 15
        cls.y = 6
        cls.z = 9
        cls.body = {"x": cls.x, "y": cls.y, "z": cls.z}

    def test_post_not_allowed(self):
        request = self.request_factory.post(self.endpoint)
        response = add_point_to_mesh(request)
        self.assertEqual(response.status_code, 405)

    def test_get_not_allowed(self):
        request = self.request_factory.get(self.endpoint)
        response = add_point_to_mesh(request)
        self.assertEqual(response.status_code, 405)

    def test_delete_not_allowed(self):
        request = self.request_factory.delete(self.endpoint)
        response = add_point_to_mesh(request)
        self.assertEqual(response.status_code, 405)

    @override_settings(INITIAL_POINTS=np.asarray([[]]))
    def test_adding_a_point_adds_point_to_initial_points_when_initial_points_are_less_than_4(self):
        request = self.request_factory.put(self.endpoint, json.dumps(self.body), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(np.equal(settings.INITIAL_POINTS, np.asarray([[self.x, self.y, self.z]])).all())
        self.assertEqual(body["message"], "Success. Added [15, 6, 9] to mesh.")

    @override_settings(INITIAL_POINTS=np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 2, 1]]))
    def test_adding_a_point_does_not_add_point_to_initial_points_when_initial_points_are_4(self):
        request = self.request_factory.put(self.endpoint, json.dumps(self.body), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(np.equal(
            settings.INITIAL_POINTS,
            np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 2, 1]])
        ).all())
        self.assertEqual(body["message"], "Success. Added [15, 6, 9] to mesh.")

    @override_settings(INITIAL_POINTS=np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1]]))
    def test_adding_a_point_does_not_add_point_to_initial_points_when_initial_points_are_greater_than_4(self):
        request = self.request_factory.put(self.endpoint, json.dumps(self.body), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(np.equal(
            settings.INITIAL_POINTS,
            np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1]])
        ).all())
        self.assertEqual(body["message"], "Success. Added [15, 6, 9] to mesh.")

    @override_settings(INITIAL_POINTS=np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1]]), GLOBAL_MESH=None)
    def test_adding_a_fourth_point_correctly_instantiates_the_global_mesh(self):
        request = self.request_factory.put(self.endpoint, json.dumps(self.body), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(settings.GLOBAL_MESH, ThreeDimensionalMesh))
        self.assertTrue(np.equal(
            settings.GLOBAL_MESH.vertices,
            np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [self.x, self.y, self.z]])
        ).all())
        self.assertEqual(body["message"], "Success. Added [15, 6, 9] to mesh.")

    def test_not_adding_a_required_parameter_returns_a_400(self):
        request = self.request_factory.put(self.endpoint, json.dumps({"x": 5}), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "Bad Request. Improperly formatted")
        self.assertContains(body["errors"], "Required parameter 'y' was not received.")
        self.assertContains(body["errors"], "Required parameter 'z' was not received.")

    def test_required_parameter_of_the_wrong_type_returns_a_400(self):
        request = self.request_factory.put(
            self.endpoint, json.dumps({"x": 5, "y": "hello", "z": [123]}), content_type="application/json"
        )

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "Bad Request. Improperly formatted")
        self.assertContains(body["errors"], "Invalid data type for parameter 'y'. A number is required.")
        self.assertContains(body["errors"], "Invalid data type for parameter 'z'. A number is required.")

    def test_non_json_body_returns_a_400(self):
        request = self.request_factory.put(self.endpoint, "x y z", content_type="text/html")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "Bad Request. Content type must be application/json.")
