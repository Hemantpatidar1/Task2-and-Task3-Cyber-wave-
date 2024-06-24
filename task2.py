import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt


data = {
    'id': [1, 2, 3, 4],
    'event': ['SOSP', 'EOSP', 'SOSP', 'EOSP'],
    'dateStamp': [43831, 43831, 43832, 43832],
    'timeStamp': [0.708333, 0.791667, 0.333333, 0.583333],
    'voyage_From': ['Port A', 'Port A', 'Port B', 'Port B'],
    'lat': [34.0522, 34.0522, 36.7783, 36.7783],
    'lon': [-118.2437, -118.2437, -119.4179, -119.4179],
    'imo_num': ['9434761', '9434761', '9434761', '9434761'],
    'voyage_Id': ['6', '6', '6', '6'],
    'allocatedVoyageId': [None, None, None, None]
}


df = pd.DataFrame(data)


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c / 1.852
    return distance


df['prev_event'] = df['event'].shift(1)
df['prev_lat'] = df['lat'].shift(1)
df['prev_lon'] = df['lon'].shift(1)
df['prev_dateStamp'] = df['dateStamp'].shift(1)
df['prev_timeStamp'] = df['timeStamp'].shift(1)

# Calculate distances and times
df['distance_travelled'] = df.apply(lambda row: calculate_distance(row['lat'], row['lon'], row['prev_lat'], row['prev_lon'])
                                    if row['prev_event'] == 'EOSP' and row['event'] == 'SOSP' else None, axis=1)
df['sailing_time'] = df.apply(lambda row: ((row['dateStamp'] - row['prev_dateStamp']) * 24 + (row['timeStamp'] - row['prev_timeStamp']) * 24)
                              if row['prev_event'] == 'EOSP' and row['event'] == 'SOSP' else None, axis=1)
df['port_stay_duration'] = df.apply(lambda row: ((row['dateStamp'] - row['prev_dateStamp']) * 24 + (row['timeStamp'] - row['prev_timeStamp']) * 24)
                                    if row['prev_event'] == 'SOSP' and row['event'] == 'EOSP' else None, axis=1)


print(df)


df['timestamp'] = pd.to_datetime(df['dateStamp'], origin='1899-12-30') + pd.to_timedelta(df['timeStamp'], unit='D')
plt.figure(figsize=(12, 6))
for index, row in df.iterrows():
    plt.plot([row['timestamp'], row['timestamp']], [0, 1], label=row['event'])

plt.xlabel('Time')
plt.ylabel('Event')
plt.title('Voyage Timeline')
plt.legend(loc='upper right')
plt.show()
