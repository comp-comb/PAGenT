# Step 1: Define Constants (Ctes.f90)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv  # Optional visualization with PyVista

# Constants
N = 100  # Number of Primary Particles
Df = 1.79  # Fractal Dimension
kf = 1.40  # Fractal Prefactor
rp_g = 15.0  # Geometric Mean PP
rp_gstd = 1.0  # Geometric PP Standard Deviation
Quantity_aggregates = 1  # Number of Aggregates
Ext_case = 0  # Extreme Cases Activation
Nsubcl_perc = 0.1  # Percentage for Subclusters
pi = np.pi  # Pi value
tol_ov = 10**-8  # Overlapping Tolerance

# Step 2: Random Sampling Functions

def randsample(arr, size):
    """ Random sample without replacement """
    return np.random.choice(arr, size=size, replace=False)


def random_normal():
    """ Generate a normal-distributed random number """
    return np.random.normal()


def lognormal_pp_radii(rp_gstd, rp_g, N):
    """ Generate Log-normal distributed radii """
    min_val = rp_g / (rp_gstd**2)
    max_val = rp_g * (rp_gstd**2)
    radii = []
    while len(radii) < N:
        value = rp_g * np.exp(np.log(rp_gstd) * random_normal())
        if min_val <= value <= max_val:
            radii.append(value)
    return np.array(radii)

# Step 3: PCA Aggregation 

def first_two_monomers(X, Y, Z, R):
    """ Initialize the first two monomers in PCA """
    X[0], Y[0], Z[0] = 0, 0, 0
    X[1], Y[1], Z[1] = R[0] + R[1], 0, 0
    return X, Y, Z


def PCA(Data, Number, R):
    """ Particle-Cluster Aggregation """
    X = np.zeros(Number)
    Y = np.zeros(Number)
    Z = np.zeros(Number)
    X, Y, Z = first_two_monomers(X, Y, Z, R)
    
    for i in range(2, Number):
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.random.uniform(0, np.pi)
        X[i] = X[i - 1] + R[i] * np.sin(phi) * np.cos(theta)
        Y[i] = Y[i - 1] + R[i] * np.sin(phi) * np.sin(theta)
        Z[i] = Z[i - 1] + R[i] * np.cos(phi)
    
    Data[:, 0], Data[:, 1], Data[:, 2], Data[:, 3] = X, Y, Z, R
    return Data

# Step 4: PCA Subclusters 

def PCA_Subclusters(Data, R, N, N_subcl):
    """ Manages PCA subclusters """
    Number_clusters = int(N / N_subcl)
    if N % N_subcl != 0:
        Number_clusters += 1
    return Number_clusters, PCA(Data, N, R)

# Step 5: CCA Aggregation 

def CCA_sub(Data, R, N):
    """ Cluster-Cluster Aggregation Algorithm """
    Number_clusters, Data = PCA_Subclusters(Data, R, N, int(N * Nsubcl_perc))
    for i in range(1, Number_clusters):
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.random.uniform(0, np.pi)
        shift_x = np.cos(theta) * np.sin(phi) * np.max(R)
        shift_y = np.sin(theta) * np.sin(phi) * np.max(R)
        shift_z = np.cos(phi) * np.max(R)
        Data[i::Number_clusters, 0] += shift_x
        Data[i::Number_clusters, 1] += shift_y
        Data[i::Number_clusters, 2] += shift_z
    return Data

# Step 6: Save Aggregates to CSV and Plot

def save_and_plot_aggregates(Data, filename="aggregates.csv", use_pyvista=False):
    """ Save the aggregate data to a CSV file and plot in 3D """
    df = pd.DataFrame(Data, columns=["X", "Y", "Z", "R"])
    df.to_csv(filename, index=False)
    
    if use_pyvista:
        plotter = pv.Plotter()
        for i in range(len(df)):
            sphere = pv.Sphere(radius=df.loc[i, "R"], center=(df.loc[i, "X"], df.loc[i, "Y"], df.loc[i, "Z"]))
            plotter.add_mesh(
                sphere,
                color="red",
                opacity=1.0,           # Adjust opacity as needed
                show_edges=False,
                smooth_shading=True,
                specular=0.2,          # Controls the specular intensity (shiny reflection)
                specular_power=100,    # Controls the size/sharpness of the specular highlight
                ambient=0.1            # Optionally adjust the ambient lighting
            )
        plotter.show()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df["X"], df["Y"], df["Z"], s=df["R"]*10, alpha=0.6)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()

