import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

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

modulation_index = 0.5  
message_signal_freq = 100e6  
message_signal = np.sin(2 * np.pi * message_signal_freq * frequency_range / max(frequency_range))  
am_modulated_signal = (1 + modulation_index * message_signal) * power_density_sq

power_at_each_frequency = am_modulated_signal * gain - noise_level

plt.figure(figure_size=(10, 6))
plt.plot(frequency_range, power_at_each_frequency, label='Modulated Power')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Density')
plt.title('Modulated Power Density vs Frequency')
plt.legend()
plt.grid(True)
plt.show()

plotter = pv.Plotter(notebook=True)
plotter.set_background('black')

x = np.linspace(0, 100, 20)
y = np.linspace(0, 100, 20)
z = np.linspace(0, 100, 20)

X, Y, Z = np.meshgrid(x, y, z)
distances = np.sqrt(X**2 + Y**2 + Z**2)

signal_strength = 1 / (distances + 1)  

points = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))
signal_strength_array = signal_strength.flatten()

plotter.add_mesh(points, scalars=signal_strength_array, cmap="viridis", opacity=[0.0, 0.6])
plotter.add_axes()
plotter.show_grid()

plotter.show()

plotter.export_obj("rf_capture.obj")

widget = pv.Plotter()
widget.add_mesh(points, scalars=signal_strength_array, cmap="viridis", opacity=[0.0, 0.6])
widget.add_axes()
widget.show()

iframe_widget = pv.Plotter()
iframe_widget.add_mesh(points, scalars=signal_strength_array, cmap="viridis", opacity=[0.0, 0.6])
iframe_widget.add_axes()
iframe_widget.show()

print(widget)
print(iframe_widget)
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
