from scipy.spatial import Delaunay
import numpy as np


class ThreeDimensionalMesh(Delaunay):
    """
    An abstraction of a 3D mesh that extends the functionality of
    [Numpy's Delaunay](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html) class.
    Some notable differences are that this implementation is assuming a "2.5D" interpretation of the mesh which
    triangulates via the x and y coordinates then projects into 3D space.
    """
    def __init__(self, vertices: np.ndarray, *args, **kwargs):
        """
        Creates a triangulated mesh
        Args:
            vertices:
        """
        # We need to triangulate via the 2D coordinates then extend to the 3D plane later to avoid a quadrahedral
        # triangulation
        self.z = vertices[:, 2]
        super().__init__(points=np.array([vertices[:, 0], vertices[:, 1]]).T, *args, **kwargs)

    @classmethod
    def load_from_file(cls, file_name: str, *args, **kwargs):
        # Trimesh is imported here because it is only used to read the file
        import trimesh
        mesh = trimesh.load(file_name)
        return cls(mesh.vertices.view(np.ndarray), *args, **kwargs)

    @property
    def vertices(self):
        return np.column_stack((self.points, self.z))

    @property
    def faces(self):
        return self.simplices

    def get_flat_vertices(self):
        return self.vertices.flatten()

    def get_flat_faces(self):
        return self.faces.flatten()

    def add_vertices(self, points: np.ndarray, *args, **kwargs):
        x_and_y = points[:, 0:2]
        z = points[:, 2]
        self.z = np.concatenate((self.z, z))
        self.add_points(x_and_y, *args, **kwargs)
