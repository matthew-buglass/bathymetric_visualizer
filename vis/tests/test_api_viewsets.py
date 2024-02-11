import json

import numpy as np
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APIRequestFactory

from vis.api_viewsets import add_point_to_mesh
from vis.models import ThreeDimensionalMesh


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
        self.assertTupleEqual(settings.INITIAL_POINTS.shape, (1, 3))
        self.assertTrue(np.equal(settings.INITIAL_POINTS, np.asarray([[self.x, self.y, self.z]])).all())
        self.assertEqual(body["message"], "Success. Added [15, 6, 9] to mesh.")

    @override_settings(INITIAL_POINTS=np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [9, 7, 12]]))
    def test_adding_a_point_does_not_add_point_to_initial_points_when_there_are_4_initial_points(self):
        request = self.request_factory.put(self.endpoint, json.dumps(self.body), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTupleEqual(settings.INITIAL_POINTS.shape, (4, 3))
        self.assertTrue(np.equal(
            settings.INITIAL_POINTS,
            np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [9, 7, 12]])
        ).all())
        self.assertEqual(body["message"], "Success. Added [15, 6, 9] to mesh.")

    @override_settings(INITIAL_POINTS=np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [9, 7, 12], [13, 7, 9]]))
    def test_adding_a_point_does_not_add_point_to_initial_points_when_there_are_more_than_4_initial_points(self):
        request = self.request_factory.put(self.endpoint, json.dumps(self.body), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 200)

        self.assertTupleEqual(settings.INITIAL_POINTS.shape, (5, 3))
        self.assertTrue(np.equal(
            settings.INITIAL_POINTS,
            np.asarray([[1, 2, 3], [2, 3, 1], [3, 2, 1], [9, 7, 12], [13, 7, 9]])
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
        request = self.request_factory.put(self.endpoint, json.dumps({"hello": "world"}), content_type="application/json")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "Bad Request. Improperly formatted")
        self.assertIn("Required parameter 'x' was not received.", body["errors"])
        self.assertIn("Required parameter 'y' was not received.", body["errors"])
        self.assertIn("Required parameter 'z' was not received.", body["errors"])

    def test_required_parameter_of_the_wrong_type_returns_a_400(self):
        request = self.request_factory.put(
            self.endpoint, json.dumps({"x": ["ack!"], "y": "hello", "z": [123]}), content_type="application/json"
        )

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "Bad Request. Improperly formatted")
        self.assertIn("Invalid data type for parameter 'x'. A number is required.", body["errors"])
        self.assertIn("Invalid data type for parameter 'y'. A number is required.", body["errors"])
        self.assertIn("Invalid data type for parameter 'z'. A number is required.", body["errors"])

    def test_non_json_body_returns_a_400(self):
        request = self.request_factory.put(self.endpoint, "x y z", content_type="text/html")

        response = add_point_to_mesh(request)
        body = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "Bad Request. Content type must be application/json.")
