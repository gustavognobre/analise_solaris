import streamlit as st
import folium
from streamlit_folium import folium_static
import requests

# Configuração inicial do Streamlit
st.set_page_config(page_title="Rota Realista em Mapa", layout="wide")

# Função para calcular e plotar a rota no mapa usando OSRM e Folium
def plot_routes(points):
    # URL base do serviço de roteamento do OSRM
    osrm_url = 'http://router.project-osrm.org/route/v1/driving/'

    # Criar um mapa centrado no primeiro ponto
    start_coords = points[0]
    mapa = folium.Map(location=start_coords, zoom_start=12)

    # Adicionar marcadores para todos os pontos
    for idx, coords in enumerate(points):
        folium.Marker(coords, popup=f'Ponto {idx + 1}').add_to(mapa)

    # Montar a URL completa para fazer a requisição ao OSRM
    waypoints_str = ";".join([f"{point[1]},{point[0]}" for point in points])
    request_url = f"{osrm_url}{waypoints_str}?overview=full&steps=true&geometries=geojson"

    # Fazer a requisição GET para obter os dados da rota
    response = requests.get(request_url)

    if response.status_code == 200:
        route_data = response.json()

        # Adicionar a rota no mapa usando Folium
        folium.features.GeoJson(route_data['routes'][0]['geometry']).add_to(mapa)
    else:
        st.error(f"Falha ao calcular a rota. Código de status: {response.status_code}")

    # Exibir o mapa usando Streamlit
    st.write("Rota seguindo as vias de trânsito:")
    folium_static(mapa)

# Função principal do aplicativo Streamlit
def Point():
    st.title('Rota Realista em Mapa')
    st.write('Visualize uma rota realista passando por todos os pontos fornecidos.')

    # Pontos específicos fornecidos
    points = [
        (-16.709996, -43.877642),
        (-16.694524, -43.868978),
        (-16.717911, -43.846506)
    ]

    # Botão para gerar a rota
    if st.button("Gerar Rota"):
        plot_routes(points)

if __name__ == '__main__':
    main()
