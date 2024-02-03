import numpy as np
from django.test import SimpleTestCase
from scipy.spatial import Delaunay

from vis.models import ThreeDimensionalMesh


class TestThreeDimensionalMesh(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_file_path = "test_data/test_mesh.stl"
        cls.bad_test_file_path = "i_do_not_exist.stl"

        # Simple pyramid geometry
        cls.pyramid_x = np.asarray([0, 0, 1, 1, 0.5])
        cls.pyramid_y = np.asarray([0, 1, 0, 1, 0.5])
        cls.pyramid_z = np.asarray([0, 0, 0, 0, 0.5])
        cls.pyramid = ThreeDimensionalMesh(
            x=cls.pyramid_x,
            y=cls.pyramid_y,
            z=cls.pyramid_z,
        )

    def test_load_from_file_works_when_file_exists(self):
        mesh = ThreeDimensionalMesh.load_from_file(self.test_file_path)
        self.assertTrue(isinstance(mesh, Delaunay))

    def test_load_from_file_raises_error_when_file_does_not_exist(self):
        self.assertRaises(ValueError, ThreeDimensionalMesh.load_from_file, self.bad_test_file_path)

    def test_loading_a_pyramid_yields_expected_vertices(self):
        expected_vertices = np.column_stack((self.pyramid_x, self.pyramid_y, self.pyramid_z))
        actual_vertices = self.pyramid.vertices

        self.assertTupleEqual(expected_vertices.shape, actual_vertices.shape)
        self.assertTrue(np.equal(expected_vertices, actual_vertices).all())

    def test_loading_a_pyramid_yields_expected_faces(self):
        expected_faces = np.asarray([
            [4, 1, 0],
            [2, 4, 0],
            [4, 3, 1],
            [3, 4, 2],
        ])
        actual_faces = self.pyramid.faces

        self.assertTupleEqual(expected_faces.shape, actual_faces.shape)
        self.assertTrue(np.equal(expected_faces, actual_faces).all())

    def test_loading_a_pyramid_yields_expected_flat_vertices(self):
        expected_vertices = np.column_stack((self.pyramid_x, self.pyramid_y, self.pyramid_z)).flatten()
        actual_vertices = self.pyramid.get_flat_vertices()

        self.assertTupleEqual(expected_vertices.shape, actual_vertices.shape)
        self.assertTrue(np.equal(expected_vertices, actual_vertices).all())

    def test_loading_a_pyramid_yields_expected_flat_faces(self):
        expected_faces = np.asarray([4, 1, 0, 2, 4, 0, 4, 3, 1, 3, 4, 2])
        actual_faces = self.pyramid.get_flat_faces()

        self.assertTupleEqual(expected_faces.shape, actual_faces.shape)
        self.assertTrue(np.equal(expected_faces, actual_faces).all())

    def test_incrementally_adding_a_point_in_the_middle_of_a_face_correctly_recalculates_the_mesh(self):
        octahedron = ThreeDimensionalMesh(
            x=self.pyramid_x,
            y=self.pyramid_y,
            z=self.pyramid_z,
            incremental=True
        )
        new_point = np.asarray([[0.25, 0.3, -0.5]])
        octahedron.add_vertices(new_point)

        expected_vertices = np.concatenate(
            (np.column_stack((self.pyramid_x, self.pyramid_y, self.pyramid_z)), new_point)
        )
        expected_flat_vertices = expected_vertices.flatten()

        expected_faces = np.asarray([
            [3, 4, 2],
            [4, 3, 1],
            [2, 5, 0],
            [4, 5, 2],
            [5, 1, 0],
            [5, 4, 1],
        ])
        expected_flat_faces = expected_faces.flatten()

        actual_vertices = octahedron.vertices
        actual_flat_vertices = octahedron.get_flat_vertices()

        actual_faces = octahedron.faces
        actual_flat_faces = octahedron.get_flat_faces()

        # Assertions
        self.assertTupleEqual(expected_vertices.shape, actual_vertices.shape)
        self.assertTrue(np.equal(expected_vertices, actual_vertices).all())

        self.assertTupleEqual(expected_faces.shape, actual_faces.shape)
        self.assertTrue(np.equal(expected_faces, actual_faces).all())

        self.assertTupleEqual(expected_flat_vertices.shape, actual_flat_vertices.shape)
        self.assertTrue(np.equal(expected_flat_vertices, actual_flat_vertices).all())

        self.assertTupleEqual(expected_flat_faces.shape, actual_flat_faces.shape)
        self.assertTrue(np.equal(expected_flat_faces, actual_flat_faces).all())
