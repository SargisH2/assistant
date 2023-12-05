import streamlit as st
from tools import handle, paste_messages

st.title("Car parts")

if 'chats' not in st.session_state:
    st.session_state['chats'] = dict()
    print('-----line 7------')####################################################

all_ids = [chat for chat in st.session_state['chats'].keys()]
chat_id = st.selectbox(
    'Select Conversation',
    (*all_ids[::-1], 'Create new'))
new_chat = (chat_id == 'Create new')

def rerun():
    global new_chat
    new_chat = True
    st.rerun()

if new_chat:
    print('-----line 22 new chat------')####################################################
    web_enabled = st.checkbox("Web search and similarity", value=False, on_change=rerun)
    chat_id = ''
else:
    print('-----line 26 old chat------')####################################################
    value = st.session_state['chats'][chat_id]['web_enabled']
    web_enabled = st.checkbox("Web search and similarity", value=value, on_change=rerun)
    paste_messages(chat_id)



if not new_chat:
    msg = st.text_input('Message: ', placeholder='Send me images')
    if st.button('Request'):
        try:
            query = msg
            id, messages = handle(query, chat_id, web = web_enabled)

            st.session_state['chats'][id]['msg'] = messages
            st.write(messages[-1])
            st.rerun()
        except Exception as e:
            print(e)
else: #new chat
    if web_enabled:
        part_1 = st.text_input('Part 1: ', placeholder='12421S') 
        part_2 = st.text_input('Part 2: ', placeholder='12421S')
        optional = st.text_input('Message: ', placeholder='Send me images')

        if st.button('Request'):
            try:
                query = f"Part 1: {part_1}, Part 2: {part_2}. " if part_1 and part_2 else ''
                query += optional
                id, messages = handle(query, chat_id)


                st.session_state['chats'][id] = dict()
                st.session_state['chats'][id]['msg'] = messages
                st.session_state['chats'][id]['web_enabled'] = True
                st.write(messages[-1])
                st.rerun()
            except Exception as e:
                print(e)
    else:
        part = st.text_input('Part: ', placeholder='12421S')
        optional = st.text_input('Message: ', placeholder='Send me images')

        if st.button('Request'):
            try:
                query = f"Part: {part}. " if part else ''
                query += optional
                id, messages = handle(query, chat_id, web = False)


                st.session_state['chats'][id] = dict()
                st.session_state['chats'][id]['msg'] = messages
                st.session_state['chats'][id]['web_enabled'] = False
                st.write(messages[-1])
                st.rerun()
            except Exception as e:
                print(e)

