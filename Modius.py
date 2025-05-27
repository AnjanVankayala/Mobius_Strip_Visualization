import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import integrate
import warnings
warnings.filterwarnings('ignore')

class MobiusStrip:
    def __init__(self, radius, width, resolution):
        #Initialize the MobiusStrip with given radius, width, and resolution
        self.radius = radius
        self.width = width
        self.resolution = resolution
        self.X, self.Y, self.Z = self._compute_mesh()

    def _compute_mesh(self):
        #Computes the mesh grid for the Mobius strip and Returns X,Y,Z coordinates for the strip
        u = np.linspace(0, 2 * np.pi, self.resolution)
        v = np.linspace(-self.width / 2, self.width / 2, self.resolution)
        U, V = np.meshgrid(u, v)

        X = (self.radius + V * np.cos(U / 2)) * np.cos(U)
        Y = (self.radius + V * np.cos(U / 2)) * np.sin(U)
        Z = V * np.sin(U / 2)

        return X, Y, Z

    def visualize(self):
        #Visualize the Mobius strip using a 3D plot
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        surf = ax.plot_surface(self.X, self.Y, self.Z, alpha=0.8, cmap='viridis', linewidth=0, antialiased=True)

        fig.colorbar(surf, shrink=0.5, aspect=5)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Mobius Strip (R={self.radius}, w={self.width})')

        ax.view_init(elev=20, azim=45)
        plt.show()

    def surface_area(self):
        #Calculates the surface area of the Mobius strip using numerical integration
        def mobius_partial_u(U, V):
            #Partial Integration with respective parameter U
            dX_dU = -((self.radius + V * np.cos(U / 2)) * np.sin(U)) - (V / 2 * np.sin(U / 2) * np.cos(U))
            dY_dU = ((self.radius + V * np.cos(U / 2)) * np.cos(U)) - (V / 2 * np.sin(U / 2) * np.sin(U))
            dZ_dU = V / 2 * np.cos(U / 2)
            return dX_dU, dY_dU, dZ_dU

        def mobius_partial_v(U):
            #Partial Integration with respective parameter V
            dX_dV = np.cos(U / 2) * np.cos(U)
            dY_dV = np.cos(U / 2) * np.sin(U)
            dZ_dV = np.sin(U / 2)
            return dX_dV, dY_dV, dZ_dV

        def dS(V, U):
            #Diffrential Area calculated with partial derivatives with respective U and V
            dX_dU, dY_dU, dZ_dU = mobius_partial_u(U, V)
            dX_dV, dY_dV, dZ_dV = mobius_partial_v(U)
            
            # Compute the cross product of the partial derivatives
            cross_product_x = dY_dU * dZ_dV - dZ_dU * dY_dV
            cross_product_y = dZ_dU * dX_dV - dX_dU * dZ_dV
            cross_product_z = dX_dU * dY_dV - dY_dU * dX_dV

            # Calculate the magnitude of the cross product vector
            magnitude = np.sqrt(cross_product_x**2 + cross_product_y**2 + cross_product_z**2)
            return magnitude

        area, _ = integrate.dblquad(dS, 0, 2 * np.pi, lambda u: -self.width / 2, lambda u: self.width / 2)

        return area

    def edge_length(self):
        #Calculate the edge length of the Mobius strip using numerical integration
        def velocity_vector_u(U, V_boundary):
            #Calculate the velocity vector of the Mobius strip's edge with respect to U at a given boundary V.
            dX_dU = -((self.radius + V_boundary * np.cos(U / 2)) * np.sin(U)) - (V_boundary / 2 * np.sin(U / 2) * np.cos(U))
            dY_dU = ((self.radius + V_boundary * np.cos(U / 2)) * np.cos(U)) - (V_boundary / 2 * np.sin(U / 2) * np.sin(U))
            dZ_dU = V_boundary / 2 * np.cos(U / 2)
            return dX_dU, dY_dU, dZ_dU

        def speed(U, V_boundary):
            dX_dU, dY_dU, dZ_dU = velocity_vector_u(U, V_boundary)
            magnitude = np.sqrt(dX_dU**2 + dY_dU**2 + dZ_dU**2)
            return magnitude

        v_boundary = self.width / 2
        edge_length, _ = integrate.quad(lambda u: speed(u, v_boundary), 0, 2 * np.pi)

        return edge_length

mobius = MobiusStrip(radius=1.0, width=0.5, resolution=30)
mobius.visualize()
area = mobius.surface_area()
edge = mobius.edge_length()
print(f"Surface Area: {area:.4f}")
print(f"Edge Length: {edge:.4f}")
