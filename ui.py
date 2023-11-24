import requests
import json
import streamlit as st

url = 'https://apiassistant.azurewebsites.net/gsearch/'

if 'chat_ids' not in st.session_state:
    st.session_state['chat_ids'] = dict()

chat_id = st.selectbox(
    'Select Conversation',
    (*[chat for chat in st.session_state['chat_ids'].keys()], 'Create new'))


def paste_messages(chat):
    if chat and chat != 'Create new':
        last_chat = st.session_state['chat_ids'][chat]
        for message in last_chat:
            try:
                role, msg = list(message.items())[0]
                st.write(f'<p><span style="color:gray">{role}:</span> {msg}</p>', unsafe_allow_html=True)
            except:
                print(message)
                st.write(f'<p>Error :( <br> try to reopen the page</p>', unsafe_allow_html=True)
paste_messages(chat_id)



req_text = st.text_input('You: ', 'Hello')
if st.button('Request'):
    if chat_id == 'Create new':
        chat_id = ''
    body = {
        "query": req_text if req_text else '',
        "chat_id": chat_id
    }

    x = requests.post(url, json = body)
    try:
        result = json.loads(x.text)
        st.session_state['chat_ids'][result['id']] = result['chat']
        st.write(result['chat'][-1])
        st.rerun()
    except Exception as e:
        print(e)

