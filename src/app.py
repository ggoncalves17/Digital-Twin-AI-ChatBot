import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

def formata_historico(mensagens):
    historico = ""
    for msg in mensagens:
        historico += f"\n{msg['role']}: {msg['content']}"
    return historico

def btn_callback(aUserPrompt):
    st.session_state.suggestedPrompt = aUserPrompt
    st.session_state.firstTime = False
  
template = """
Responde à questão abaixo.

Aqui está o histórico da conversa: {context}

Questão: {question}

Resposta:
 
"""

# A ALTERAÇÃO PARA O MODELO PRETENDIDO É FEITA AQUI -------------
model = OllamaLLM(model="mygemma3v2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

st.title('DIGITAL TWIN - AI CHATBOT')

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'firstTime' not in st.session_state:
    st.session_state.firstTime = True
if 'suggestedPrompt' not in st.session_state:
    st.session_state.suggestedPrompt = None

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])   

userPrompt = st.chat_input('Write your question here...')

if st.session_state.suggestedPrompt:
    userPrompt = st.session_state.suggestedPrompt

if st.session_state.firstTime is True and userPrompt is None:    
    st.button(label="Como te chamas?", on_click=btn_callback, args=("Como te chamas?",))
    st.button(label="Tens quantos anos?", on_click=btn_callback, args=("Tens quantos anos?",))
    st.button(label="Qual é a tua profissão?", on_click=btn_callback, args=("Qual é a tua profissão?",))

historico = formata_historico(st.session_state.messages)

if userPrompt:

    st.session_state.firstTime = False
    st.session_state.suggestedPrompt = None

    st.chat_message('user').markdown(userPrompt)    

    # print("HISTÓRICO: ", historico)

    result = chain.invoke({"context": historico, "question": userPrompt})

    st.session_state.messages.append({'role': 'user', 'content': userPrompt})

    st.chat_message('assistant').markdown(result)

    st.session_state.messages.append({'role': 'assistant', 'content': result})


