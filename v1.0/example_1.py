import json
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set your API access token here
your_access_token = "your-access-token"

# Read the input file for the noise calculation
with open('noise_input.json') as fp:
    input_data = json.load(fp)

# Extract the segments from the input data
segments = pd.DataFrame(data=input_data['segments']['data'], columns=input_data['segments']['columns'])

# Visualize the segments, the first point is intentionally left out to make the image more clear
plt.figure('ground_track')
plt.title('Ground track for the JETFAC verification case')
plt.plot(segments['x2'], segments['y2'], 'r-', label='ground track')

# Extract the observers from the input data
observers = np.array(input_data['observers'])

# Visualize the observers
plt.figure('ground_track')
plt.title('Ground track and observers for the JETFAC verification case')
plt.scatter(observers[:, 0], observers[:, 1], marker='d', label='observers')
plt.ylabel('x-coordinates [m]')
plt.xlabel('y-coordinates [m]')
plt.legend()
plt.axis('equal')
plt.show()

# Extract the NPD data from the input data
metric_data = pd.DataFrame(data=input_data['metric_data']).set_index('name')

# Visualize the SEL NPD data
plt.figure('sel_npd_data')
plt.title('SEL NPD data for the JETFAC verification case')
npd_data = pd.DataFrame(
    data=metric_data.loc['sel', 'npd']['data'],
    columns=metric_data.loc['sel', 'npd']['columns'],
    index=metric_data.loc['sel', 'npd']['index']
)
for thrust_setting, nd_data in npd_data.iterrows():
    plt.plot(nd_data.index, nd_data, marker='x', label='P={}'.format(thrust_setting))
plt.xscale('log')
plt.ylabel('SEL [dBA]')
plt.xlabel('distance [m]')
plt.legend()
plt.show()

# Visualize the LAmax NPD data
plt.figure('lamax_npd_data')
plt.title(r'$L_{A,max}$ NPD data for the JETFAC verification case')
npd_data = pd.DataFrame(
    data=metric_data.loc['lamax', 'npd']['data'],
    columns=metric_data.loc['lamax', 'npd']['columns'],
    index=metric_data.loc['lamax', 'npd']['index']
)
for thrust_setting, nd_data in npd_data.iterrows():
    plt.plot(nd_data.index, nd_data, marker='x', label='P={}'.format(thrust_setting))
plt.xscale('log')
plt.ylabel(r'$L_{A,max}$ [dBA]')
plt.xlabel('distance [m]')
plt.legend()
plt.show()

# Create a data string for the requests
data = json.dumps(input_data)

# Perform the call to the /validation endpoint to make sure that the input data meets all the requirements for a noise
# calculation
validation_response = requests.post('https://echo.aerlabs.com/v1.0/validate', data=data, headers={
    "Authorization": "Bearer " + your_access_token,
    "Content-Type": "application/json"
})

# It should return an HTTP status code 200
print(validation_response.status_code)

# The body should contain a message that says that there are no errors in your input data
print(validation_response.json())

# Perform the call to the /noise endpoint
noise_response = requests.post('https://echo.aerlabs.com/v1.0/noise', data=data, headers={
    "Authorization": "Bearer " + your_access_token,
    "Content-Type": "application/json"
})

# It should return an HTTP status code 200
print(noise_response.status_code)

# The body should contain the noise levels for each observer
print(noise_response.json())
