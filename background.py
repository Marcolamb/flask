
import time
import requests
import pandas as pd
import sqlite3


def obtainData():
    conn = sqlite3.connect('test.db')

    response = requests.get('https://restcountries.com/v3.1/all')

    # case: status code 200
    if response.status_code == 200:
        data = response.json()

        # Extract the country names
        country_names = [entry['name']['common'] for entry in data]

        # Specify the keys to include in the JSON
        keys_to_include = ['name.common', 'independent', 'status', 'unMember', 'capital', 'region',
                           'subregion', 'landlocked', 'borders', 'area', 'population', 'fifa',
                           'timezones', 'continents']

        # Filter the JSON to include only the specified keys
        filtered_data = [{key: value for key, value in entry.items() if key in keys_to_include}
                        for entry in data]

        # Convert data into a DataFrame for further analysis
        df = pd.json_normalize(filtered_data)
        df['name.common'] = country_names

        toReplace = ['capital', 'borders', 'timezones', 'continents']
        df[toReplace] = df[toReplace].astype(str).apply(lambda x: x.str.replace('[', '').str.replace(']', '').str.replace("'", ''))

        df.to_sql('countries', conn, if_exists='replace', index=False)

    conn.close()


startTime = time.time()
obtainData()
    
while(True):
    try:
        if time.time() - startTime > 86400:
            obtainData()
            startTime = time.time()

    except KeyboardInterrupt: 
        break
    
    except Exception as e:
        print(e)
        break

    