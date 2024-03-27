from numpy.typing import NDArray
from scipy.spatial import Delaunay
import numpy as np


class ThreeDimensionalMesh(Delaunay):
    """
    An abstraction of a 3D mesh that extends the functionality of
    [Numpy's Delaunay](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html) class.
    Some notable differences are that this implementation is assuming a "2.5D" interpretation of the mesh which
    triangulates via the x and y coordinates then projects into 3D space.
    """
    def __init__(self, vertices: np.ndarray = None, incremental: bool = False, *args, **kwargs):
        """
        Creates a triangulated mesh
        Args:
            vertices: an array with the shape (,3), where each element is a vertex in 3D space
            incremental: Allow adding new points incrementally. This takes up some additional resources.
        """
        # We need to triangulate via the 2D coordinates then extend to the 3D plane later to avoid a quadrahedral
        # triangulation
        self.z = vertices[:, 2]
        super().__init__(
            points=vertices[:, 0:2],
            incremental=incremental,
            *args,
            **kwargs)

        # Showing the density of information
        self.density_map = np.asarray([[False] * self.density_map_size()] * self.density_map_size(), dtype=bool)
        self.min_x = -10
        self.max_x = 10
        self.min_y = -10
        self.max_y = 10

    @staticmethod
    def density_map_size() -> int:
        return 64

    @classmethod
    def load_from_file(cls, file_name: str, *args, **kwargs):
        """

        Args:
            file_name: The path to the 3D file to open. Accepts any file that
            [Trimesh's load](https://trimesh.org/trimesh.html#trimesh.load) accepts.

        Returns:
            mesh: an instance of ThreeDimensionalMesh
        """
        # Trimesh is imported here because it is only used to read the file
        import trimesh
        mesh = trimesh.load(file_name)
        return cls(mesh.vertices.view(np.ndarray), *args, **kwargs)

    @property
    def vertices(self) -> NDArray:
        """
        The 3D points of the mesh

        Returns:
            vertices: an array of shape (,3), where each element is a vertex in 3D space
        """
        return np.column_stack((self.points, self.z))

    @property
    def faces(self) -> NDArray[np.int32]:
        """
        The indexes of the vertices that form faces.

        Returns:
            faces: an array of shape (,3), where each element is the 3 indexes into vertices that are connected to
            form a face
        """
        return self.simplices

    @property
    def htlm_density_map(self):
        """

        Returns:

        """
        size = self.density_map_size()
        img = np.asarray([[False] * size] * size, dtype=bool)

        for x, y in self.points:
            x_idx = int((x - self.min_x) / (self.max_x - self.min_x) * (size - 1))
            y_idx = int((y - self.min_y) / (self.max_y - self.min_y) * (size - 1))
            x_idx = max(0, min(x_idx, (size - 1)))
            y_idx = max(0, min(y_idx, (size - 1)))
            img[x_idx][y_idx] = True

        return img.tolist()

    def get_flat_vertices(self) -> NDArray:
        """
        The vectorized form of the vertices

        Returns:
            vertices: an array of shape (1,), where each element is a co-ordinate location. Elements in groups of 3
            (ex. 0, 1, and 2) form the x, y, and z components of a point.
        """
        return self.vertices.flatten()

    def get_flat_faces(self) -> NDArray[np.int32]:
        """
        The vectorized form of the faces

        Returns:
            faces: an array of shape (1,), where each element is an index into vertices. Elements in groups of 3
            (ex. 0, 1, and 2) form the indexes of a face
        """
        return self.faces.flatten()

    def add_vertices(self, vertices: np.ndarray, *args, **kwargs) -> None:
        """
        Adds a collection of vertices to the mesh and re-triangulates

        Args:
            vertices: an array of shape (,3), where each element is a vertex in 3D space
        """
        x_and_y = vertices[:, 0:2]
        z = vertices[:, 2]
        self.z = np.concatenate((self.z, z))
        self.add_points(x_and_y, *args, **kwargs)
        for x, y in x_and_y:
            self.update_min_and_max(x, y)

    def update_min_and_max(self, x, y):
        """

        Args:
            x:
            y:

        Returns:

        """
        self.min_x = min(x, self.min_x)
        self.max_x = max(x, self.max_x)
        self.min_y = min(y, self.min_y)
        self.max_y = max(y, self.max_y)
