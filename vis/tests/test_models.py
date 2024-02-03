import numpy as np
import trimesh
from django.test import SimpleTestCase
from scipy.spatial import Delaunay

from vis.models import ThreeDimensionalMesh


class TestMesh(SimpleTestCase):
    def setUp(self):
        self.test_file_path = "test_data/test_mesh.stl"
        self.bad_test_file_path = "i_do_not_exist.stl"

    def test_load_from_file_works_when_file_exists(self):
        mesh = ThreeDimensionalMesh.load_from_file(self.test_file_path)
        self.assertTrue(isinstance(mesh, Delaunay))

    def test_load_from_file_raises_error_when_file_does_not_exist(self):
        self.assertRaises(ValueError, ThreeDimensionalMesh.load_from_file, self.bad_test_file_path)
