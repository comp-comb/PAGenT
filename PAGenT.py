#!/usr/bin/env python3
"""
GUI for the Aggregate Simulation

This file creates a Tkinter GUI that lets the user set parameters for the simulation
and then runs the aggregation algorithm. It calls functions from the simulation module,
which is assumed to be saved as 'aggregation_simulation.py' in the same directory.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Import simulation functions from your simulation code.
# Make sure the simulation code (aggregation_simulation.py) is in the same folder.
from aggregation_simulation import (
    lognormal_pp_radii,
    randsample,
    CCA_sub,
    save_and_plot_aggregates,
)

def run_simulation():
    """Read parameters from the GUI and run the aggregation simulation."""
    try:
        # Read and convert parameters from the GUI entries
        N = int(entry_N.get())
        # Although Df and kf are defined in the simulation module, they are not used in the calculations.
        Df = float(entry_Df.get())
        kf = float(entry_kf.get())
        rp_g = float(entry_rp_g.get())
        rp_gstd = float(entry_rp_gstd.get())
        Nsubcl_perc = float(entry_Nsubcl.get())
        csv_filename = entry_csv.get()
        use_pyvista = bool(var_pyvista.get())

        # Update status in the GUI
        status_label.config(text="Running simulation, please wait...")
        root.update_idletasks()

        # Generate the primary particle radii
        R = lognormal_pp_radii(rp_gstd, rp_g, N)
        R = randsample(R, N)

        # Initialize Data array and perform the CCA aggregation
        Data = np.zeros((N, 4))
        Data = CCA_sub(Data, R, N)

        # Save the aggregate data to a CSV file and plot in 3D
        save_and_plot_aggregates(Data, filename=csv_filename, use_pyvista=use_pyvista)

        # Update status and notify the user
        status_label.config(text="Simulation completed successfully!")
        messagebox.showinfo("Success", "CCA Aggregation Completed!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
        status_label.config(text="Error during simulation.")


# ---------------------------
# Set up the main GUI window
# ---------------------------
root = tk.Tk()
root.title("Aggregate Simulation GUI")

# Create a frame to hold the input fields and buttons
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

# --- Parameter: Number of Primary Particles ---
ttk.Label(main_frame, text="Number of Primary Particles (N):").grid(row=0, column=0, sticky=tk.W, pady=2)
entry_N = ttk.Entry(main_frame, width=15)
entry_N.grid(row=0, column=1, pady=2)
entry_N.insert(0, "100")

# --- Parameter: Fractal Dimension (Df) ---
ttk.Label(main_frame, text="Fractal Dimension (Df):").grid(row=1, column=0, sticky=tk.W, pady=2)
entry_Df = ttk.Entry(main_frame, width=15)
entry_Df.grid(row=1, column=1, pady=2)
entry_Df.insert(0, "1.79")

# --- Parameter: Fractal Prefactor (kf) ---
ttk.Label(main_frame, text="Fractal Prefactor (kf):").grid(row=2, column=0, sticky=tk.W, pady=2)
entry_kf = ttk.Entry(main_frame, width=15)
entry_kf.grid(row=2, column=1, pady=2)
entry_kf.insert(0, "1.40")

# --- Parameter: Geometric Mean PP (rp_g) ---
ttk.Label(main_frame, text="Geometric Mean PP (rp_g):").grid(row=3, column=0, sticky=tk.W, pady=2)
entry_rp_g = ttk.Entry(main_frame, width=15)
entry_rp_g.grid(row=3, column=1, pady=2)
entry_rp_g.insert(0, "15.0")

# --- Parameter: Geometric PP Std Dev (rp_gstd) ---
ttk.Label(main_frame, text="Geometric PP Std Dev (rp_gstd):").grid(row=4, column=0, sticky=tk.W, pady=2)
entry_rp_gstd = ttk.Entry(main_frame, width=15)
entry_rp_gstd.grid(row=4, column=1, pady=2)
entry_rp_gstd.insert(0, "1.0")

# --- Parameter: Subcluster Percentage (Nsubcl_perc) ---
ttk.Label(main_frame, text="Subcluster Percentage (Nsubcl_perc):").grid(row=5, column=0, sticky=tk.W, pady=2)
entry_Nsubcl = ttk.Entry(main_frame, width=15)
entry_Nsubcl.grid(row=5, column=1, pady=2)
entry_Nsubcl.insert(0, "0.1")

# --- Parameter: CSV Filename ---
ttk.Label(main_frame, text="CSV Filename:").grid(row=6, column=0, sticky=tk.W, pady=2)
entry_csv = ttk.Entry(main_frame, width=15)
entry_csv.grid(row=6, column=1, pady=2)
entry_csv.insert(0, "aggregates.csv")

# --- Option: Use PyVista for 3D Visualization ---
var_pyvista = tk.IntVar(value=1)
check_pyvista = ttk.Checkbutton(main_frame, text="Use PyVista for 3D Visualization", variable=var_pyvista)
check_pyvista.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=2)

# --- Run Simulation Button ---
run_button = ttk.Button(main_frame, text="Run Simulation", command=run_simulation)
run_button.grid(row=8, column=0, columnspan=2, pady=10)

# --- Status Label ---
status_label = ttk.Label(main_frame, text="Ready")
status_label.grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=2)

# Configure resizing behavior
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Start the GUI event loop
root.mainloop()
