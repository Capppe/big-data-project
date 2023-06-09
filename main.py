import numbers as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('vehicles.csv')

#############################################################
# Display 80 columns in Jupyter notebooks
#############################################################
pd.set_option('display.max_columns', 80)

#############################################################
# Display general car info as the first few columns
#############################################################
custom_cols = [ 
    'make',
    'model',
    'eng_dscr',
    'drive',
    'fuelType1',
    'trany',
    'year'
 ]

cols = data.columns.tolist()
for i in range(len(custom_cols)):
    cols.insert(i, cols.pop(cols.index(custom_cols[i])))

data = data.reindex(columns=cols)

data

#############################################################
# Display only rows that contain 'Volvo'
#############################################################
volvo_rows = data[data['make'] == 'Volvo']

#volvo_rows
#data


#############################################################
# Display average mileage per year per car + emissions
#############################################################
data['year'] = pd.to_datetime(data['year'], format='%Y')
data['l/100'] = 235.2146 / data['comb08']
data['g/km'] = data['co2TailpipeGpm'] / 1.60934

fuel_consumption = data.groupby(data['year'].dt.year)['l/100'].mean()
emissions = data.groupby(data['year'].dt.year)['g/km'].mean()
emissions = emissions * 0.1

plt.plot(fuel_consumption.index, fuel_consumption.values, label='Fuel consumption (l/100km)')
plt.plot(emissions.index, emissions.values, label='Emissions - CO2 (g/100m)')
plt.xlabel('Year')
plt.ylabel('Average')
plt.title('Average fuel consumption and Emissions per Year')
plt.legend()
plt.show()

#############################################################
# Display what car has the best mileage per year
#############################################################
no_electric = data[data['charge120'] == 0.0]
no_electric = no_electric[no_electric['charge240'] == 0.0]

no_electric['year'] = pd.to_datetime(data['year'], format='%Y')

grouped = no_electric.groupby('year')

best_vehicles = []
best_mpgs = []

for year, group in grouped:
    best_vehicle_index = group['comb08'].idxmax()
    best_vehicle = group.loc[best_vehicle_index, 'model']
    best_mpg = group.loc[best_vehicle_index, 'comb08']
    best_vehicles.append(best_vehicle)
    best_mpgs.append(best_mpg)

plt.figure(figsize=(10,10))
plt.xlabel('Year')
plt.ylabel('MPG')
plt.title('Best MPG Vehicle by Year')
plt.scatter(no_electric['year'].unique(), best_mpgs, color='red', label='Best MPG')

for i, txt in enumerate(best_vehicles):
    plt.annotate(txt, (no_electric['year'].unique()[i], best_mpgs[i]), rotation=60)

plt.legend()
plt.show()

#############################################################
# Display what car has the worst mileage per year
#############################################################
no_electric = data[data['charge120'] == 0.0]
no_electric = no_electric[no_electric['charge240'] == 0.0]

no_electric['year'] = pd.to_datetime(data['year'], format='%Y')

grouped = no_electric.groupby('year')

best_vehicles = []
best_mpgs = []

for year, group in grouped:
    best_vehicle_index = group['comb08'].idxmin()
    best_vehicle = group.loc[best_vehicle_index, 'model']
    best_mpg = group.loc[best_vehicle_index, 'comb08']
    best_vehicles.append(best_vehicle)
    best_mpgs.append(best_mpg)

plt.figure(figsize=(10,10))
plt.xlabel('Year')
plt.ylabel('MPG')
plt.title('Worst MPG Vehicle by Year')
plt.scatter(no_electric['year'].unique(), best_mpgs, color='blue', label='Worst MPG')

for i, txt in enumerate(best_vehicles):
    plt.annotate(txt, (no_electric['year'].unique()[i], best_mpgs[i]), rotation=60)

plt.legend()
plt.show()

#############################################################
# Display with a pie graph how many times a manufacturer were at the top of emissions 
#############################################################

data_emi = data[['year', 'make', 'co2TailpipeGpm']]

data_emi

min_emissions = data_emi.groupby('year')['co2TailpipeGpm'].idxmin()

min_emissions

manufacturer_least_emi = data_emi.loc[min_emissions, 'make']

manufacturer_count = manufacturer_least_emi.value_counts()

manufacturer_least_emi

manufacturer_count

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct

plt.figure(figsize=(8, 8))
plt.pie(manufacturer_count, labels=manufacturer_count.index, autopct=make_autopct(manufacturer_count))
plt.title('Manufacturer with Least Emissions Each Year')
plt.axis('equal')
plt.show()