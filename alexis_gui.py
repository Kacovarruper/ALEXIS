# import streamlit as st
# from langchain_ollama import OllamaLLM

# # 1. Configuración de página (SIEMPRE PRIMERO)
# st.set_page_config(page_title="Alexis OS", layout="wide")

# # 2. INICIALIZACIÓN DE SESIÓN (EL FIX DEFINITIVO)
# # Aquí aseguramos que tanto el motor como la lista de mensajes existan ANTES de cualquier lógica
# if "llm" not in st.session_state:
#     st.session_state.llm = OllamaLLM(model="llama3")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 3. INTERFAZ VISUAL
# st.title("Proyecto A.L.E.X.I.S")
# st.subheader("Capa de Interfaz: Online")
# st.markdown("---")

# # 4. RENDERIZAR HISTORIAL
# # Esto dibuja los mensajes que ya existen en la lista
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # 5. LÓGICA DE INTERACCIÓN
# if prompt := st.chat_input("¿Qué analizamos hoy, Caleb?"):
#     # Añadir el mensaje de Caleb a la interfaz y a la memoria
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Respuesta de Alexis
#     with st.chat_message("assistant"):
#         placeholder = st.empty()
#         full_response = ""
        
#         try:
#             # Efecto de streaming tipo Jarvis
#             for chunk in st.session_state.llm.stream(prompt):
#                 full_response += chunk
#                 placeholder.markdown(full_response + "▌")
            
#             # Limpiar el cursor final
#             placeholder.markdown(full_response)
#             # GUARDAR en la lista que causaba el error
#             st.session_state.messages.append({"role": "assistant", "content": full_response})
            
#         except Exception as e:
#             st.error(f"Error en el núcleo de Alexis: {e}")

import streamlit as st
from langchain_ollama import OllamaLLM
import os

# 1. Configuración de página
st.set_page_config(page_title="Alexis OS", layout="wide")

# 2. Inicialización de sesión
if "llm" not in st.session_state:
    st.session_state.llm = OllamaLLM(model="llama3")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "codigo_contexto" not in st.session_state:
    st.session_state.codigo_contexto = ""

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Panel de Control")
    st.subheader("Ingesta de Código")
    ruta_archivo = st.text_input("Pega la ruta completa del archivo .cs:")
    
    if st.button("Analizar Archivo"):
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                content = f.read()
                st.session_state.codigo_contexto = content
                st.success(f"Archivo cargado: {os.path.basename(ruta_archivo)}")
        else:
            st.error("Ruta no válida. Revisa el path.")
    
    if st.button("Limpiar Memoria"):
        st.session_state.messages = []
        st.session_state.codigo_contexto = ""
        st.rerun()

# --- INTERFAZ PRINCIPAL ---
st.title("Proyecto A.L.E.X.I.S")
st.caption("Sensei de .NET Core 8 | Arquitecto Senior")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lógica de Chat
if prompt := st.chat_input("¿Qué analizamos hoy, Caleb?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # --- EL ADN DE ALEXIS CON CONTEXTO ---
        contexto_sistema = f"""
        Eres 'Alexis', el Sensei de Programación de Caleb. 
        Experto en .NET Core 8, C#, Clean Architecture, expero en tailwind,
        boostrap y con un profundo conocimiento en mejoras de rendimiento sobre entornos de programacion a escala, expero en SQL SERVER y MySQL.

        CONTEXTO DEL CÓDIGO ACTUAL:
        {st.session_state.codigo_contexto if st.session_state.codigo_contexto else "No se ha cargado código aún."}

        PREGUNTA DE CALEB: {prompt}
        """

        try:
            for chunk in st.session_state.llm.stream(contexto_sistema):
                full_response += chunk
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")