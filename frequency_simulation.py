import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt


power_watts = 100
surface_area = 0.1
clock_speed = 64e6 
program_mem_size = 128000
data_mem_size = 1536

# Simulate 65% processor utilization
utilization_factor = 0.65
clock_speed *= utilization_factor
power_watts *= utilization_factor 

frequency_range = np.linspace(2e14, 4e14, 500)

power_density_sq = power_watts / surface_area

gain = np.full(frequency_range.shape, 10)
noise_level = np.sqrt(frequency_range) / 1000

# Adjust power consumption based on processor utilization
power_consumption = np.random.uniform(50, 200, size=frequency_range.shape) * utilization_factor

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

x = np.linspace(0, 100, 20)
y = np.linspace(0, 100, 20)
z = np.linspace(0, 100, 20)

X, Y, Z = np.meshgrid(x, y, z)
distances = np.sqrt(X**2 + Y**2 + Z**2)

# Adjust signal strength calculation to account for processor utilization
signal_strength = (1 / (distances + 1)) * utilization_factor  

points = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))
signal_strength_array = signal_strength.flatten()


plotter = pv.Plotter(notebook=False)
plotter.set_background('white')  # Set background for better contrast

# Add mesh with larger points
plotter.add_mesh(points, scalars=signal_strength_array, cmap="viridis", point_size=10, render_points_as_spheres=True, opacity=[0.0, 0.6])

# Set camera to overlook the scene, maybe this is the problem
plotter.camera_position = [(150, 150, 150), (50, 50, 50), (0, 0, 1)]  


plotter.show(auto_close=False)


depth_image = plotter.get_image_depth()


plotter.close()

plt.figure(figsize=(10, 8))
plt.imshow(depth_image, cmap='gray')
plt.colorbar(label='Depth')
plt.title('Depth Image')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

grid.save("rf_sim.obj")
