import json
import random
import sys
# this code is to create random ecg value for uploading
# Set up parameters for the ECG waveform
SAMPLE_RATE = 150 # Hz
DURATION = 10 # seconds
NUM_SAMPLES = SAMPLE_RATE * DURATION
AMPLITUDE = 1 # volts

# Generate an array of random values between -1 and 1
ecg_values = [random.uniform(-1, 1) for _ in range(NUM_SAMPLES)]

# Scale the values and round to two decimal places
scaled_values = [round((value * AMPLITUDE + sys.float_info.epsilon), 2) for value in ecg_values]

# Create a JSON object with the scaled values
ecg_data = {
    "ecg": {
        "sampleRate": SAMPLE_RATE,
        "duration": DURATION,
        "values": scaled_values
    }
}

with open('ecg_data2.json', 'w') as outfile:
    json.dump(ecg_data, outfile)