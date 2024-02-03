from scipy.spatial import Delaunay
import numpy as np


class ThreeDimensionalMesh(Delaunay):
    def __init__(self, x, y, z, *args, **kwargs):
        self.z = z
        super().__init__(points=np.array([x, y]).T, *args, **kwargs)

    @classmethod
    def load_from_file(cls, file_name: str, *args, **kwargs):
        import trimesh
        mesh = trimesh.load(file_name)
        verts = mesh.vertices.view(np.ndarray)
        return cls(x=verts[:, 0], y=verts[:, 1], z=verts[:, 2], *args, **kwargs)

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
