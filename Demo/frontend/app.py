import streamlit as st
import requests
import json
import httpx
import aiohttp

from config import (
    BACKEND_URL,
    PDF_LIST,
    BOT_ICON_URL,
    USER_ICON_URL,
)


def st_init() -> None:
    st.set_page_config(
        page_title="PDF-Chat Demo",
        layout="centered",
        page_icon=":books:",
    )

    st.header(":red[Multiple PDF] Chat Demo :sunglasses:")


def post_userinput(query: str, options: list[str]) -> None:
    url = BACKEND_URL + "/question"
    userinput = {"question": query, "options": options}

    #response = await aiohttp.request(url=url, json=userinput)
    response = requests.post(url=url, json=userinput)
    print(f"Got the response. Respone code is [{response.status_code}]")

    if response.status_code == 200:
        content_str = response.content.decode("utf-8")
        content_json = json.loads(content_str)
        return content_json
            
# async def post_userinput(query: str, options: list[str]) -> None:
#     url = BACKEND_URL + "/question"
#     userinput = {"question": query, "options": options}

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json=userinput)
#         print(f"Got the response. Response code is [{response.status_code}]")

#         if response.status_code == 200:
#             content_str = response.content.decode("utf-8")
#             content_json = json.loads(content_str)
#             return content_json


def print_chat_history() -> None:
    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            avatar = BOT_ICON_URL
        elif message["role"] == "user":
            avatar = USER_ICON_URL

        with st.chat_message(message["role"], avatar=avatar):
            if type(message['content']) == str:
                st.write(message["content"])

            else:
                st.write(message["content"]['response'])
                
                if 'ref_docs' in message["content"]:
                    st.json(message["content"]['ref_docs'], expanded=False)
                elif 'subqa' in message["content"]:
                    st.json(message["content"]['subqa'], expanded=False)
                else:
                    st.write(message['content'].keys())
                    st.write("아웃풋 출력 실패")


def handle_userinput(user_question: str, options: list[str]) -> None:
    """
    사용자 입력값(user_question, options)을 받아 답변을 받아옵니다.
    사용자의 질문과 답변을 채팅로그에 기록합니다.
    """
    with st.chat_message("user", avatar=USER_ICON_URL):
        st.write(user_question)

    st.session_state.chat_history.append({"role": "user", "content": user_question})

    # response 생성 후 채팅로그에 저장, 출력
    with st.chat_message("assistant", avatar=BOT_ICON_URL):
        with st.spinner("답변 생성중입니다. 답변에 몇 분 정도 시간이 소요될 수 있습니다."):
            response = post_userinput(user_question, options)
        st.write(response)
        response_type = response['type']
                    
        if 'ref_docs' in response:
            st.json(response['ref_docs'], expanded=False)
        elif 'subqa' in response:
            st.json(response['subqa'], expanded=False)


    
    st.session_state.chat_history.append({"role": "assistant", "content":response})


def main():
    st_init()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        options = st.multiselect("PDF select", PDF_LIST, max_selections=2)

    print_chat_history()

    user_question = st.chat_input("여기에 질문을 입력하세요:", disabled=False)
    if user_question and options:
        print("User Question [" + user_question + "]")
        print("PDF files", options)
        st.chat_input("답변 생성 중에는 질문을 입력할 수 없습니다.", disabled=True)
        handle_userinput(user_question=user_question, options=options)
        st.experimental_rerun()


if __name__ == "__main__":
    main()
