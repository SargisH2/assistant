import streamlit as st
from tools import handle

if 'chat_ids' not in st.session_state:
    st.session_state['chat_ids'] = dict()

all_ids = [chat for chat in st.session_state['chat_ids'].keys()]
chat_id = st.selectbox(
    'Select Conversation',
    (*all_ids[::-1], 'Create new'))


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


part_1 = st.text_input('Part number 1: ', placeholder='12421S')
part_2 = st.text_input('Part number 2: ', placeholder='12421S')
optional = st.text_input('Other message: ', placeholder='Thank You')
if st.button('Request'):
    if chat_id == 'Create new':
        chat_id = ''
    try:
        query = f"part nuber 1: {part_1} part nuber 2: {part_2}. I need images and similarity scores." if part_1 and part_2 else ''
        query += optional
        id, messages = handle(query, chat_id)


        st.session_state['chat_ids'][id] = messages
        st.write(messages[-1])
        st.rerun()
    except Exception as e:
        print(e)



