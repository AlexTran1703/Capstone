import matplotlib.pyplot as plt
import numpy as np

# Set up plot and parameters
plt.ion()
fig, ax = plt.subplots()
t = np.arange(0, 10, 1/250)  # generate time array
line, = ax.plot(t, np.zeros_like(t))

# Start loop to update plot
while True:
    # Generate random ECG data for demo purposes
    ecg_signal = np.random.normal(0, 1, size=len(t))
    line.set_ydata(ecg_signal)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
