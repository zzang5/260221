import streamlit as st
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="내 자기소개 페이지", page_icon="👋", layout="centered")

# 2. 사이드바 (연락처 및 링크)
st.sidebar.header("Contact Info")
st.sidebar.text("📧 email@example.com")
st.sidebar.text("🔗 [GitHub](https://github.com)")
st.sidebar.text("📝 [Blog](https://blog.com)")

# 3. 메인 화면 - 헤더 부분
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    # 본인의 사진 파일명으로 변경하세요 (예: 'profile.jpg')
    # 사진이 없다면 placeholder 이미지를 사용합니다.
    #st.image("https://via.placeholder.com/150", width=150) 
     st.image("https://i.namu.wiki/i/_HHTYdKOuG6QdskbyW5ZwepiZw3mplg47y7mA21SEezw96xd2hrzF-JY2euBBKOBRky8Jv4Rb1qv0My_t0U1VQ.webp", 
             caption="나를 나타내는 사진",
             use_container_width=True)

with col2:
    st.title("안녕하세요, 홍길동입니다!")
    st.subheader("성장을 즐기는 데이터 분석가 / 개발자")

st.divider()

# 4. 자기소개 본문
st.header("📌 About Me")
st.write("""
안녕하세요! 저는 데이터를 통해 문제를 해결하고 새로운 가치를 만드는 것에 열정을 가진 **홍길동**입니다.  
현재 Streamlit을 활용해 아이디어를 빠르게 웹으로 구현하는 연습을 하고 있습니다.
""")

# 5. 기술 스택 (컬럼 활용)
st.header("🛠 Tech Stack")
tag1, tag2, tag3, tag4 = st.columns(4)
tag1.button("Python", use_container_width=True)
tag2.button("Streamlit", use_container_width=True)
tag3.button("SQL", use_container_width=True)
tag4.button("PyTorch", use_container_width=True)

# 6. 간단한 프로젝트/경력 섹션
st.header("🚀 Projects")
with st.expander("내 생애 첫 Streamlit 웹앱"):
    st.write("Streamlit을 사용하여 5분 만에 자기소개 페이지를 배포했습니다.")

# 7. 하단 푸터
st.caption("© 2026 Gildong Hong. Built with Streamlit")
