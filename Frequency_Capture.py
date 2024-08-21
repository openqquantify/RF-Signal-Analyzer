import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import pyvista as pv
from pyvista import Plotter

# All samples for SDR are hypothetical, these numbers must be changed to match use case
sdr = RtlSdr()
sdr.sample_rate = 2.048e6  
sdr.center_freq = 100e6    
sdr.freq_correction = 60  
sdr.gain = 'auto'         

plotter = Plotter()
plotter.set_background('black')

grid_size = 100
z_scale = 1e-6
x = np.linspace(-sdr.sample_rate / 2, sdr.sample_rate / 2, grid_size)
y = np.linspace(0, 10, grid_size)

grid = pv.StructuredGrid()
grid.points = np.array(np.meshgrid(x, y, np.zeros(grid_size))).T.reshape(-1, 3)
grid.dimensions = (grid_size, grid_size, 1)

def update_plot():
    samples = sdr.read_samples(256*1024) # Any real-time updating could be cpu intensive, just be aware
    fft_size = len(samples)
    window = np.blackman(fft_size)
    fft_result = np.fft.rfft(window * samples)
    fft_abs = np.abs(fft_result)
    power_density = 10 * np.log10(fft_abs**2 / fft_size)

    z_values = np.tile(power_density[:grid_size] * z_scale, grid_size).reshape(grid.dimensions)
    grid.points[:, 2] = z_values.flatten()

    plotter.update_coordinates(grid.points, render=True)

try:
    while True:
        update_plot()
        plotter.show(auto_close=False)
except KeyboardInterrupt:
    print("Interrupted by user, closing SDR")
finally:
    sdr.close()
    plotter.close()

    # Save the grid as an OBJ file
    grid.save("rf_capture.obj")
