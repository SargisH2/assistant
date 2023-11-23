import requests
import json
import streamlit as st

url = 'https://apiassistant.azurewebsites.net/gsearch/'

req_text = st.text_input('Your text: ', 'Hello')
flag_new = st.checkbox('New chat')

if 'chat_id' not in st.session_state:
    st.session_state['chat_id'] = ''
chat_id = st.text_input('id: ', st.session_state['chat_id'])

if st.button('Request'):
    if flag_new:
        st.session_state['chat_id'] = ''
    body = {
        "query": req_text if req_text else '',
        "chat_id": chat_id
    }

    x = requests.post(url, json = body)
    try:
        result = json.loads(x.text)
    except Exception as e:
        result = e
    st.session_state['chat_id'] = result['id']
    
    st.write(result)