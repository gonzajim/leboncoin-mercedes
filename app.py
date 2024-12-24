import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página a scrapear
url = "https://www.leboncoin.fr/recherche?category=2&u_car_brand=MERCEDES-BENZ&u_car_model=MERCEDES-BENZ_Classe%20GLC&gearbox=2&vehicle_damage=undamaged&regdate=2015-max&mileage=min-150000"

# Encabezados para la solicitud HTTP
headers = {'User-Agent': 'Mozilla/5.0'}

# Realizar la solicitud HTTP
response = requests.get(url, headers=headers)
response.raise_for_status()  # Verificar si la solicitud fue exitosa

# Analizar el contenido HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Extraer los datos de los anuncios
anuncios = soup.find_all('div', class_='ad_class')  # Reemplaza 'ad_class' con la clase real

# Lista para almacenar los datos
datos = []

for anuncio in anuncios:
    titulo = anuncio.find('h2', class_='title_class').get_text(strip=True)  # Reemplaza 'title_class' con la clase real
    precio = anuncio.find('span', class_='price_class').get_text(strip=True)  # Reemplaza 'price_class' con la clase real
    km = anuncio.find('span', class_='km_class').get_text(strip=True)  # Reemplaza 'km_class' con la clase real
    año = anuncio.find('span', class_='year_class').get_text(strip=True)  # Reemplaza 'year_class' con la clase real
    motor = anuncio.find('span', class_='motor_class').get_text(strip=True)  # Reemplaza 'motor_class' con la clase real
    datos.append([titulo, precio, km, año, motor])

# Crear un DataFrame con los datos
df = pd.DataFrame(datos, columns=['Título', 'Precio', 'KM', 'Año', 'Motor'])

# Limpiar y convertir la columna de precios a numérico
df['Precio'] = df['Precio'].str.replace('€', '').str.replace(' ', '').astype(float)

# Ordenar el DataFrame por precio ascendente
df = df.sort_values(by='Precio')

# Configurar la aplicación Streamlit
st.title('Anuncios de Mercedes-Benz Clase GLC')
st.dataframe(df)
