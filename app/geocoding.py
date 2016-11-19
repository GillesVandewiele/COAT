import geopy
import pandas as pd
from geopy.geocoders import GoogleV3
import numpy as np

insurance_df = pd.read_csv('data/data_insurance.csv')
new_df_columns = insurance_df.columns.values
new_df_columns = np.append(new_df_columns, ['Lng', 'Lat'], 0)
new_df = pd.DataFrame(columns=new_df_columns)

geolocator = GoogleV3()
for i in range(len(insurance_df)):
    address = ' '.join(insurance_df.iloc[i, :][['GL-Address', 'GL-City', 'Country']].values)
    geolocation = geolocator.geocode(address)
    if geolocation is None:
        print('FAIL')

    new_df.loc[i] = np.append(insurance_df.loc[i], [geolocation.longitude, geolocation.latitude], 0)

print(new_df)
new_df.to_csv('data/data_insurance_geocoords.csv', index=False)
