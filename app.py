from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 1. Configuración del motor
llm = OllamaLLM(model="llama3")

# 2. El Prompt Maestro (Personalidad de Alexis)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres 'Alexis', el Sensei de Programación de Caleb. Experto en .NET Core 8, Clean Architecture y SQL Server. Tu tono es de Arquitecto Senior: crítico, técnico y muy útil."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")
])

chain = prompt | llm

# 3. Almacén de memoria de la sesión
chat_history = []

def chat_con_alexis():
    print("\n" + "="*50)
    print("SISTEMA ALEXIS ONLINE - MODO INTERACTIVO")
    print("Escribe 'salir' para finalizar o 'limpiar' para olvidar el historial.")
    print("="*50 + "\n")

    while True:
        # Entrada de Caleb
        user_input = input("Caleb > ")

        if user_input.lower() == "salir":
            print("\nAlexis: 'Entendido, Caleb. Estaré aquí cuando necesites revisar más arquitectura. Éxito.'")
            break
        
        if user_input.lower() == "limpiar":
            chat_history.clear()
            print("\nAlexis: 'Memoria de sesión borrada.'\n")
            continue

        print("\nAlexis está analizando...\n")

        # Ejecución con Streaming
        full_response = ""
        for chunk in chain.stream({"question": user_input, "chat_history": chat_history}):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        # Guardamos en la memoria para que Alexis "recuerde"
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=full_response))
        print("\n" + "-"*30 + "\n")

if __name__ == "__main__":
    chat_con_alexis()

