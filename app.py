import streamlit as st
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

# Verificar el estado de la respuesta
if result.status_code == 200:
    # Procesar el contenido de la página
    # Implementa aquí la lógica para extraer los datos relevantes
    # y construir el DataFrame de pandas con las columnas deseadas
    # Por ejemplo:
    datos = [
        {"Título": "Ejemplo 1", "Precio": 20000, "KM": 150000, "Año": 2015, "Motor": "Diesel"},
        {"Título": "Ejemplo 2", "Precio": 25000, "KM": 120000, "Año": 2016, "Motor": "Gasolina"},
        # Agrega más datos según lo extraído
    ]
    df = pd.DataFrame(datos)
    df = df.sort_values(by="Precio")

    # Mostrar los datos en Streamlit
    st.title("Anuncios de Mercedes-Benz Clase GLC")
    st.dataframe(df)
else:
    st.error(f"Error al acceder a la página: {result.status_code}")
