#!/usr/bin/env python

from datetime import date
import streamlit as st
import pandas as pd
import requests

base_url = 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Covid19CountyStatisticsHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=CountyName,PopulationCensus16,ConfirmedCovidCases,PopulationProportionCovidCases&outSR=4326&f=json'
response = requests.get(base_url)
print(response)
get_json_response = requests.get(base_url).json()

#  finding the outer most keys 
# print(list(get_json_response))

#  'features' is the key holding the values I want

data = []
for i in get_json_response['features']:
    data.append(i)

# List comprehension
new_data = [i['attributes'] for i in data]
# Normal loop below
# for i in range(len(data)):
#     for key in data:
#         new_data.append(key['attributes'])

#  All variables below containing lists of data from api request
county_names = [i['CountyName'] for i in new_data]
population_total_2016 = [i['PopulationCensus16'] for i in new_data]
confirmed_cases = [i['ConfirmedCovidCases'] for i in new_data]

infection_rate = []
for i in range(0, 26):
    i = round((population_total_2016[i] / confirmed_cases[i]), 2)
    infection_rate.append(i)

population_minus_infected = []
for i in range(0, 26):
    i = population_total_2016[i] - confirmed_cases[i]
    population_minus_infected.append(i)

pandas_table = {
    'County': county_names,
    'Population': population_total_2016,
    'Confirmed cases': confirmed_cases,
    'Infected rate %': infection_rate
}

st.title('Covid-19 live cases web-app (Ireland)')
st.subheader('Created by Daniel Lambert')
# st.write('')
st.write('''
The data located in the table below has been taken via an api created by the Irish government.
The table consists of various values that are represented via bar charts for easier readability further down the page.
''')

df = pd.DataFrame(pandas_table)
st.write(df)

st.write('''
Bar chart 1 - Shows the population of each county 
with the infected population highlighted on top.
''')
st.write('Note: Dublin(5) has a population more than twice the size of the next biggest county.')

total_case_chart = {
    'County': county_names,
    'Population unharmed': population_minus_infected,
    'Confirmed cases': confirmed_cases
}

df = pd.DataFrame(total_case_chart)
df = df.groupby('County')[['Population unharmed', 'Confirmed cases']].sum()
st.bar_chart(df)


st.write('''
Bar chart 2 - Shows the percentage of people 
that are infected in each county.
''')
st.write('Note: Wicklow(25) my home county has the largest infection rate (Published 18.12.21).')

infected_percentage = {
    'County': county_names,
    'Infected rate (%)': infection_rate,
}
total_cases_df = pd.DataFrame(infected_percentage)
total_cases_df = total_cases_df.groupby('County')['Infected rate (%)'].sum()
st.bar_chart(total_cases_df)

myslider = st.slider('Celsius to Fahrenheit calculator')
st.write(myslider, 'degrees celcius in Fahrenheit is', myslider * 9/5 +32 )