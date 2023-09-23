import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
import time

# create a new Qt application
app = QApplication(sys.argv)

# create a new plot widget
pw = pg.PlotWidget()

# add the plot widget to the window
pw.show()

# create a new plot curve
curve = pw.plot()

# set x-axis range
pw.setXRange(0, 1000)

# pre-fill data to start with
data_buffer = np.zeros(1000)
curve.setData(data_buffer)

# start the animation loop
while True:
    # read new ECG data from sensor or file
    # replace this with your own code
    new_data = np.random.normal(size=20)

    # shift data buffer by the length of new data
    data_buffer[:-20] = data_buffer[20:]

    # add new data at the end of the buffer
    data_buffer[-20:] = new_data

    # update the plot with new data
    curve.setData(data_buffer)

    # force the Qt event loop to update
    app.processEvents()

    # pause briefly to simulate real-time display
    time.sleep(0.01)
