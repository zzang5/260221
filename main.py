import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="대한민국 100대 명산 트래킹 가이드", layout="wide")

@st.cache_data
def load_data():
    # CSV 파일 로드 (인코딩은 파일 상태에 따라 cp949 또는 utf-8-sig 사용)
    df = pd.read_csv('산림청 국립자연휴양림관리소_숲나들e 숲길 100대명산 정보_20250421.csv', encoding='cp949')
    # 결측치 제거 및 좌표 데이터 숫자형 변환
    df = df.dropna(subset=['X좌표', 'Y좌표'])
    return df

data = load_data()

st.title("🌲 대한민국 100대 명산 트래킹 안내소")
st.markdown("지도의 마커에 마우스를 올리면 산 이름을, 클릭하면 상세 정보를 볼 수 있습니다.")

# 사이드바: 지역 선택 필터
all_provinces = ["전체"] + sorted(data['명산_소재지'].str.split().str[0].unique().tolist())
selected_province = st.sidebar.selectbox("지역(도/시)을 선택하세요", all_provinces)

if selected_province != "전체":
    filtered_data = data[data['명산_소재지'].str.contains(selected_province)]
else:
    filtered_data = data

# 메인 화면 레이아웃
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📍 {selected_province} 명산 지도")
    
    # 지도 중심 설정 (데이터가 있으면 첫 번째 데이터 기준, 없으면 전국 기준)
    if not filtered_data.empty:
        start_lat = filtered_data['Y좌표'].mean()
        start_lon = filtered_data['X좌표'].mean()
    else:
        start_lat, start_lon = 36.5, 127.5

    # Folium 지도 생성
    m = folium.Map(location=[start_lat, start_lon], zoom_start=7, control_scale=True)

    # 마커 추가
    for _, row in filtered_data.iterrows():
        # 팝업에 들어갈 HTML 내용 (산 개요 등)
        popup_html = f"""
        <div style='width:250px'>
            <h4>{row['명산_이름']}</h4>
            <b>높이:</b> {row['명산_높이']}m<br>
            <b>난이도:</b> {row['난이도']}<br>
            <p style='font-size:12px'>{row['산_개요'][:100]}...</p>
        </div>
        """
        
        folium.Marker(
            location=[row['Y좌표'], row['X좌표']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['명산_이름'], # 마우스를 올렸을 때 나오는 정보
            icon=folium.Icon(color='green', icon='tree', prefix='fa')
        ).add_to(m)

    # Streamlit에 지도 표시
    st_folium(m, width=800, height=600)

with col2:
    st.subheader("🔍 상세 리스트")
    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            with st.expander(f"{row['명산_이름']} ({row['명산_소재지'].split()[0]})"):
                st.write(f"**높이:** {row['명산_높이']}m")
                st.write(f"**특징:** {row['특징_및_선정_이유']}")
                st.write(f"**산행코스:** {row['산행코스']}")
    else:
        st.write("해당 지역의 데이터가 없습니다.")

---
st.caption("데이터 출처: 산림청 국립자연휴양림관리소 (숲나들e)")
