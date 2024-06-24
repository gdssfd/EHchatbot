from langchain_community.llms import Ollama
import streamlit as st
import time

# 모델 초기화
llm = Ollama(model="llama2")

# 배경 이미지 설정
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20210828/pngtree-alpaca-color-paper-watercolor-animal-torn-paper-background-image_772149.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# 세션 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("🦙 Ollama", "안녕하세요! 무엇을 도와드릴까요?")]

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "font_size" not in st.session_state:
    st.session_state.font_size = 16

if "last_interaction" not in st.session_state:
    st.session_state.last_interaction = ""

if "user_name" not in st.session_state:
    st.session_state.user_name = "닉네임"  # 기본 닉네임 설정

def add_to_chat_history(user_input, bot_response):
    st.session_state.chat_history.append((st.session_state.user_name, user_input))
    st.session_state.chat_history.append(("🦙 Ollama", bot_response))

def display_chat_history():
    for speaker, message in st.session_state.chat_history:
        if speaker == st.session_state.user_name:
            st.markdown(f"""
            <div style='text-align: left; background-color: #ffffff; padding: 10px; border-radius: 10px; border: 2px solid #bbbbbb; margin-bottom: 10px; font-size: {st.session_state.font_size}px;'>
                <strong>{speaker}</strong>: {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: right; background-color: #eeeeee; padding: 10px; border-radius: 10px; border: 2px solid #bbbbbb; margin-bottom: 10px; font-size: {st.session_state.font_size}px;'>
                <strong>{speaker}</strong>: {message}
            </div>
            """, unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    # 로고 이미지
    st.image("https://cloudfront-ap-northeast-1.images.arcpublishing.com/chosunbiz/4VTMIGOICP2DUYW6ZUWVKEDET4.png", use_column_width=True)
    st.header("Ollama와 대화하기")
    st.markdown(
        """
        <p style='font-size: 14px;'>Ollama가 답변을 작성할 때 폰트 사이즈를 수정하면 Ollama가 작동을 멈춥니다. 이용에 참고하여주세요.</p>
        """, 
        unsafe_allow_html=True
    )
    
    # 닉네임 입력 받기
    user_name_input = st.text_input("당신의 이름을 알려주세요!", st.session_state.user_name)
    if user_name_input:
        st.session_state.user_name = user_name_input

    # 폰트 크기 슬라이더
    new_font_size = st.slider("폰트 크기", min_value=10, max_value=30, value=st.session_state.font_size)
    if new_font_size != st.session_state.font_size:
        st.session_state.font_size = new_font_size
        st.session_state.last_interaction = "slider"

# 사이드바 css
sidebar_style = '''
<style>
    .css-1lcbmhc {
        background-color: #ffffff;
        border: 2px solid #bbbbbb;
        padding: 20px;
        border-radius: 10px;
    }
</style>
'''

st.markdown(sidebar_style, unsafe_allow_html=True)

# 레이아웃
chat_placeholder = st.empty()  # 채팅 기록 표시용
input_placeholder = st.empty()  # 입력 필드 표시용

with chat_placeholder.container():
    display_chat_history()

with input_placeholder.container():
    # 사용자 입력 필드
    user_input = st.text_input(
        " ", 
        value=st.session_state.user_input, 
        placeholder="Ollama와 대화해보세요!", 
        key="user_input",
        help="대화를 입력해주세요.",
    )

if st.session_state.user_input and st.session_state.last_interaction != "slider":
    st.session_state.last_interaction = "input"
    # Ollama 답변 로딩
    st.session_state.chat_history.append(("🦙 Ollama", "답변을 찾고 있어요. 잠시만 기다려 주세요!"))
    chat_placeholder.empty()
    with chat_placeholder.container():
        display_chat_history()

    # 응답받기
    bot_response = llm.invoke(st.session_state.user_input)

    # 로딩 메시지 제거
    st.session_state.chat_history.pop()

    # 대화 기록에 추가
    add_to_chat_history(st.session_state.user_input, bot_response)

    # 대화 기록 표시 업데이트
    chat_placeholder.empty()
    with chat_placeholder.container():
        display_chat_history()
