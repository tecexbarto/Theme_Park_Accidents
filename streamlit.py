import streamlit as st
import pandas as pd
import plotly.express as px

#cargamos los datos
data = pd.read_csv('data_rev.csv')

#incluimos una portada
st.image('portada.jpg', use_column_width=True)

#añadimos el título 
st.title(':blue[Universal Florida/Disney World Incident Data (2002-2022)]')

#creamos un filtro para seleccionar el año y filtramos por el año seleccionado
selected_year = st.selectbox('Select a year:', sorted(data['Year'].unique()))
data_year = data[data['Year'] == selected_year]

#creamos las variables para almacenar el número de accidentados y de fallecidos
num_accidents = data_year.shape[0]
num_deaths = data_year[data_year['Passed_away'] == 'Yes'].shape[0]

#creamos un encabezado que muestre los estadísticos del año seleccionado
st.header(f'Statistics for the year {selected_year}')

#si hay más de un registro para el año seleccionado, mostramos el slider de edad
if data_year.shape[0] > 1:
    min_age = data_year['Age'].min()
    max_age = data_year['Age'].max()

    #creamos un slider que filtre por edad
    age_range = st.slider('Select age range:', min_value=min_age, max_value=max_age, value=(min_age, max_age))

    data_year = data_year[(data_year['Age'] >= age_range[0]) & (data_year['Age'] <= age_range[1])]

    #mostramos la edad única si solo hay un registro para el año seleccionado
else:
    unique_age = data_year['Age'].iloc[0]
    st.write(f'Age of the incident: {unique_age}')

#mostramos el número total de accidentes y muertes en el año
st.write(f'🤕 Total number of accidents: {num_accidents}')
if num_deaths > 0:
    st.write(f'💀 Total number of deaths: {num_deaths}')
else:
    st.write('💀 No deaths this year')

#hacemos una lista con los meses ordenados cronológicamente, y luego la convertimos en un tipo de dato categórico para asegurarnos de que los meses se muestren en el orden deseado
months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
data_year['Month_name'] = pd.Categorical(data_year['Month_name'], categories=months_order, ordered=True)

#creamos un gráfico de barras con el número de accidentes por mes
accidents_by_month = data_year.groupby('Month_name').size().reset_index(name='Accidents')
fig_month = px.bar(accidents_by_month, x='Month_name', y='Accidents', title=f'Number of accidents per month in {selected_year}', category_orders={'Month_name': months_order})
fig_month.update_layout(xaxis_title='Month')
st.plotly_chart(fig_month)

#creamos un gráfico de tipo sunburst con el número de accidentes por complejo de ocio, parque temático y atracción
df_recopilatorio = data_year.groupby(['Company', 'Theme_Park', 'Ride_name']).size().reset_index(name='Count')
color_map = {'Universal Studios': '#1E90FF', 'Disney World': '#00008B' }
fig_sunburst = px.sunburst(df_recopilatorio, path=['Company', 'Theme_Park', 'Ride_name'], values='Count', title=f'Theme park accidents in {selected_year}', color='Company', color_discrete_map=color_map)
fig_sunburst.update_layout(title=f'Theme park accidents in {selected_year}', width=1200, height=1000)
st.plotly_chart(fig_sunburst)

#creamos un gráfico tipo donut con el número de accidentes por género
df_sexo = data_year.groupby('Gender').size().reset_index(name='Count')
fig_gender = px.pie(df_sexo, values='Count', names='Gender', title=f'Accidents by gender in {selected_year}', hole=0.5)
st.plotly_chart(fig_gender)



