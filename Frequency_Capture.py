import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr


sdr = RtlSdr()
sdr.sample_rate = 2.048e6  # Set sample rate (depends on your device)
sdr.center_freq = 100e6    
sdr.freq_correction = 60  
sdr.gain = 'auto'         


def update_line(num, sdr, line):
    samples = sdr.read_samples(256*1024)
    fft_size = len(samples)
    window = np.blackman(fft_size)
    fft_result = np.fft.rfft(window * samples)
    fft_abs = np.abs(fft_result)
    power_density = fft_abs**2 / fft_size
    freqs = np.fft.rfftfreq(fft_size, d=1./sdr.sample_rate)
    
    x = np.linspace(-sdr.sample_rate/2, sdr.sample_rate/2, fft_size)
    
    line.set_ydata(power_density)  
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)


ax.set_xlim(-sdr.sample_rate/2, sdr.sample_rate/2)
ax.set_ylim(-100, -20)
ax.grid()

plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Density (dB)')
plt.title('Real-time Spectrum Analysis')


try:
    while True:
        update_line(0, sdr, line)
        plt.pause(0.01)
        plt.draw()
except KeyboardInterrupt:
    print("Interrupted by user, closing SDR...")
finally:
    sdr.close()

