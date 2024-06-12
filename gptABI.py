import streamlit as st
import openai
import json
import requests

# Set up the page configuration
st.set_page_config(layout="wide")


# Crear las columnas
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("https://res.cloudinary.com/ddmifk9ub/image/upload/v1714666361/OFI/Logos/ofi-black.png")

with col2:
    st.title("Ofi Services Assistant")

with col3:
    st.image("https://brandworld.ab-inbev.com/sites/g/files/wnfebl3996/files/Style%20Guide/MicrosoftTeams-image%20%282%29.png")


openai.api_key = st.secrets["OPENAI_API_KEY"]

# Cargar la configuración del modelo
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Inicializar los mensajes de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para cargar el JSON de gestión de proyectos desde GitHub
@st.cache_data
def load_project_management_info(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error(f"Error al obtener el JSON: {response.status_code}")
        st.stop()

    try:
        return response.json()
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar JSON: {e.msg}")
        st.stop()

# URL del archivo JSON en GitHub
json_url = "https://github.com/Vansik4/PV-ai/blob/main/PV%20(1).json"

# Cargar la información del proyecto
project_info = load_project_management_info(json_url)

# Convertir el JSON en una cadena de texto
project_info_text = json.dumps(project_info, indent=2)

# Crear un prompt inicial personalizado
initial_prompt = (
    "You are a highly knowledgeable data assistant specializing in logistics, supply chain management, and accounts payable processes. You have access to a dataset "
    "containing detailed information about transport orders, their status, responsible individuals, providers, and various logistical metrics. This dataset includes "
    "columns such as:\n"
    "Year of Planning (Año Planificacion)\n"
    "Transport Order ID (Transporte)\n"
    "Order ID (Pedido)\n"
    "Provider ID (Id Proveedor)\n"
    "Status of Liquidation (Estatus De Liquidacion)\n"
    "Criticality (Criticidad)\n"
    "Service (Servicio)\n"
    "Area Responsible (Responsable De Area)\n"
    "Folio Responsible (Responsable De Folio)\n"
    "Provider (Proveedor)\n"
    "Origin (Origen)\n"
    "Destination (Destino)\n"
    "General Expenses (GeEs)\n"
    "Tariff in USD (Tarifa Usd)\n"
    "Planning End Date (FinPlanif)\n"
    "Days between Planning and Movement (Dias entre Plan. y Mov.)\n"
    "Actual Movement Date (FeSM Real)\n"
    "Days between Movement and Liquidation (Dias entre Mov. y Liq.)\n"
    "New Liquidation Date (Fecha Liquidacion (Nueva))\n"
    "Days between Planning and Liquidation (Dias entre Plan. y Liq.)\n"
    "Days (Dias)\n"
    "Liquidated (Liquidado)\n"
    "Month (Mes)\n\n"
    f"{project_info_text}\n\n"
    "If you receive a greeting like 'hi' or 'hello', introduce yourself by saying, 'Hello, I am the assistant specializing in logistics, supply chain management, and accounts payable processes. How can I assist you today?'\n\n"
    "Please respond to questions in a clear and straightforward manner, avoiding technical jargon and focusing on practical, easy-to-understand information based on the provided dataset.")

# Show a welcome message and description
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    with st.chat_message("assistant"):
        st.markdown("I am a virtual assistant specializing in project management. "
                    "You can ask me questions about project management, "
                    "important dates, team members, budget, and more.")

# Display chat history
st.header("Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me a question about project management"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    # Llamar a la API de OpenAI para obtener la respuesta
    with st.chat_message("assistant"):
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        response = openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages
        )
        response_text = response.choices[0].message.content
        # Mostrar la respuesta del asistente
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})