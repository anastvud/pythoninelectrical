import pandas as pd
import numpy as np

data = pd.read_csv('test_01.csv', sep = ';')



time_differences = np.diff(time)
average_time_step = np.mean(time_differences)
sampling_rate = 1 / average_time_step

print(f"Sampling Rate: {sampling_rate} Hz")