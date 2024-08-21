import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

# All numbers are hypothetical for development purposes
power_watts = 100
surface_area = 0.1          
clock_speed = 64e6
program_mem_size = 128000
data_mem_size = 1536

frequency_range = np.linspace(2e14, 4e14, 500) 

power_density_sq = power_watts / surface_area

gain = np.full(frequency_range.shape, 10) 
noise_level = np.sqrt(frequency_range) / 1000

power_consumption = np.random.uniform(50, 200, size=frequency_range.shape)

device_levels = {
    "power_density_sq": power_density_sq,
    "gain": gain,
    "noise_level": noise_level,
    "power_consumption": power_consumption,
    "power_watts": power_watts,
    "surface_area": surface_area,
    "clock_speed": clock_speed,
    "program_mem_size": program_mem_size,
    "data_mem_size": data_mem_size
}

power_at_each_frequency = power_density_sq * gain - noise_level

plt.figure(figsize=(10, 6))
plt.plot(frequency_range, power_at_each_frequency, label='Power')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Density')
plt.title('Power Density vs Frequency')
plt.legend()
plt.grid(True)
plt.show()

plotter = pv.Plotter()
plotter.set_background('black')

grid_size = len(frequency_range)
x = frequency_range
y = power_at_each_frequency
z = power_consumption  # Arbitrary example to add a third dimension

points = np.column_stack((x, y, z))
mesh = pv.PolyData(points)

plotter.add_mesh(mesh, render_points_as_spheres=True, point_size=5, color='white')
plotter.add_axes()
plotter.show_grid()

plotter.show()

mesh.save("simulation_result.obj")
