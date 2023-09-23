import numpy as np
import os
import wfdb
import tensorflow as tf
from biosppy.signals import ecg
from wfdb import processing
import collections
import tensorflow_addons as tfa
from sklearn import preprocessing
def process_data(signal):
    #len(signal)/30
    if signal[-1] <= 200:   
        sampling = signal[-1]
    else:
        sampling = 360
    signal = np.array(signal)
    signal, resampled_t = processing.resample_sig(signal, sampling, 125)
    ecgdata = signal
    data = ecg.ecg(signal, sampling_rate= 125 , show=False)
    pro_data, num_beat = ecg.extract_heartbeats(signal, data[2], sampling_rate= 125, before = 0, after = 0.96)
    return pro_data, ecgdata, data[2]

def normalize_ECG(signal):
    #nor_sig = np.zeros((signal.shape[0], signal.shape[1]), dtype = float)
    #for i in range(len(signal)):
        #nor_sig[i] = processing.normalize_bound(signal[i], lb=0, ub=1)
    nor_sig = preprocessing.normalize(signal, axis = 0, norm = 'max')
    return nor_sig

def zero_to_nan(array):
    """ Return nan for any value = 0"""
    return [float('nan') if x==0 else x for x in array]

#187
def data_convert(signal):
    multi_heartbeat = np.zeros((1,187), dtype = float)
    for i in range(signal.shape[0]):
        heartbeat = signal[i]
        heartbeat = np.append(heartbeat, np.zeros((1, 187 - (signal.shape[1])), dtype = float))
        multi_heartbeat = np.insert(multi_heartbeat, -1, heartbeat, axis = 0)
    multi_heartbeat = np.delete(multi_heartbeat, -1, axis = 0)
    return multi_heartbeat

def predict(signal, file):
    model = tf.keras.models.load_model(file)
    signal = signal.reshape(signal.shape[0], signal.shape[1], 1)
    output = model.predict(signal)
    model_output = np.argmax(output, axis = 1)
    model_output = np.ndarray.tolist(model_output)
    #print(model_output)
    
    
    #print(type(model_output))
    #count = collections.Counter(model_output)
    #print(f"Count = {count}")
    return model_output


#def predict(signal, file):
#    model = tf.keras.models.load_model(file)
#    signal = signal.reshape(signal.shape[0], signal.shape[1], 1)
#    output = model.predict(signal)
#    model_output = np.argmax(output, axis=1)
#    count = collections.Counter(model_output)
#    # Convert the Counter object to a list of (key, value) tuples
#    count = dict(count)
#    output_list = [f"{k}: {v}" for k, v in count.items()]
#    return output_list

    