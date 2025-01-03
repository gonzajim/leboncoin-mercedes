import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
from scrapfly import ScrapflyClient, ScrapeConfig

# Obtener la clave de API desde los secretos
api_key = st.secrets["scrapfly_api_key"]

# Inicializar el cliente de Scrapfly con la clave de API
scrapfly = ScrapflyClient(key=api_key)

# Configurar la solicitud de scraping
scrape_config = ScrapeConfig(
    url="https://www.leboncoin.fr/recherche?category=2&u_car_brand=MERCEDES-BENZ&u_car_model=MERCEDES-BENZ_Classe%20GLC&gearbox=2&vehicle_damage=undamaged&regdate=2015-max&mileage=min-150000",
    asp=True,  # Activa el procesamiento anti-scraping
    render_js=True  # Renderiza JavaScript si es necesario
)

# Realizar la solicitud de scraping
result = scrapfly.scrape(scrape_config)

if result.status_code == 200:
    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(result.content, 'html.parser')

    # Extraer descripciones
    potential_descriptions = soup.find_all(string=lambda text: text and ('Mercedes' in text or 'GLC' in text))

    # Extraer precios
    potential_prices = soup.find_all(string=lambda text: text and '\u20ac' in text)

    # Extraer kilometraje
    potential_kilometers = soup.find_all(string=lambda text: text and 'km' in text)

    # Extraer enlaces
    potential_links = soup.find_all('a', href=True)
    detail_links = [
        f"https://www.leboncoin.fr{link['href']}" for link in potential_links if '/ad/voitures/' in link['href']
    ]

    # Combinar los datos extraídos
    cars = []
    for description, price, km, link in zip(potential_descriptions, potential_prices, potential_kilometers, detail_links):
        cars.append({
            'Descripción': description.strip(),
            'Precio': price.strip().replace('\u202f', '').replace('\xa0', '').replace('€', '').strip(),
            'Kilometraje': km.strip().replace(' km', '').replace('\u202f', '').strip(),
            'Enlace': f"[Ver anuncio]({link})"
        })

    # Crear un DataFrame
    car_data = pd.DataFrame(cars)

    # Convertir columnas a valores numéricos donde sea necesario
    car_data['Precio'] = pd.to_numeric(car_data['Precio'], errors='coerce')
    car_data['Kilometraje'] = pd.to_numeric(car_data['Kilometraje'], errors='coerce')

    # Agregar filtros para limitar resultados por precio y kilometraje
    st.sidebar.header("Filtros")
    min_price = st.sidebar.number_input("Precio mínimo", value=int(car_data['Precio'].min()), step=1000)
    max_price = st.sidebar.number_input("Precio máximo", value=int(car_data['Precio'].max()), step=1000)
    min_km = st.sidebar.number_input("Kilometraje mínimo", value=int(car_data['Kilometraje'].min()), step=1000)
    max_km = st.sidebar.number_input("Kilometraje máximo", value=int(car_data['Kilometraje'].max()), step=1000)

    # Aplicar los filtros
    filtered_data = car_data[(car_data['Precio'] >= min_price) & (car_data['Precio'] <= max_price) &
                             (car_data['Kilometraje'] >= min_km) & (car_data['Kilometraje'] <= max_km)]

    # Ordenar por precio
    filtered_data = filtered_data.sort_values(by='Precio')

    # Mostrar los resultados en Streamlit con capacidad de ordenar
    st.title("Tabla de coches")
    st.dataframe(filtered_data, use_container_width=True)
else:
    st.error(f"Error al acceder a la página: {result.status_code}")
