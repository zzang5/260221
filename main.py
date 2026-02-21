import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="대한민국 100대 명산 트래킹 가이드", layout="wide")

@st.cache_data
def load_data():
    file_path = '산림청 국립자연휴양림관리소_숲나들e 숲길 100대명산 정보_20250421.csv'
    try:
        # 인코딩 문제 해결 (cp949 우선 시도)
        df = pd.read_csv(file_path, encoding='cp949')
    except:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # 좌표 데이터 숫자형 변환 및 결측치 제거
    df['X좌표'] = pd.to_numeric(df['X좌표'], errors='coerce')
    df['Y좌표'] = pd.to_numeric(df['Y좌표'], errors='coerce')
    df = df.dropna(subset=['X좌표', 'Y좌표'])
    return df

try:
    data = load_data()

    st.title("🌲 대한민국 100대 명산 트래킹")
    st.markdown("마우스를 올리면 **산 이름**이, 클릭하면 **산행시간 및 정보**가 나타납니다.")

    # 사이드바: 지역 선택
    provinces = ["전체"] + sorted(data['명산_소재지'].str.split().str[0].unique().tolist())
    selected_province = st.sidebar.selectbox("지역을 선택하세요", provinces)

    if selected_province != "전체":
        filtered_data = data[data['명산_소재지'].str.contains(selected_province)]
    else:
        filtered_data = data

    col1, col2 = st.columns([2, 1])

    with col1:
        # 지도 중심 설정
        center_lat = filtered_data['Y좌표'].mean() if not filtered_data.empty else 36.5
        center_lon = filtered_data['X좌표'].mean() if not filtered_data.empty else 127.5
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

        for _, row in filtered_data.iterrows():
            # 난이도 컬럼에서 산행시간 정보 추출 (데이터에 포함된 내용 활용)
            course_time = row['난이도'] if pd.notnull(row['난이도']) else "정보 없음"
            
            # 클릭 시 나타날 팝업 내용 구성
            popup_html = f"""
            <div style="width:200px; font-family: 'Malgun Gothic';">
                <h4 style="margin-bottom:5px;">{row['명산_이름']}</h4>
                <b>📏 높이:</b> {row['명산_높이']}m<br>
                <b>⏱️ 산행시간:</b> {course_time}<br>
                <hr style="margin:10px 0;">
                <small>소재지: {row['명산_소재지']}</small>
            </div>
            """
            
            folium.Marker(
                location=[row['Y좌표'], row['X좌표']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=row['명산_이름'], # 마우스 호버 시 산 이름 표시
                icon=folium.Icon(color='green', icon='mountain', prefix='fa')
            ).add_to(m)

        st_folium(m, width="100%", height=600)

    with col2:
        st.subheader("⛰️ 상세 리스트")
        if not filtered_data.empty:
            for _, row in filtered_data.iterrows():
                with st.expander(f"{row['명산_이름']} ({row['명산_높이']}m)"):
                    st.write(f"**⏱️ 산행시간/난이도:** {row['난이도']}")
                    st.write(f"**📍 위치:** {row['명산_소재지']}")
                    st.write(f"**📝 특징:** {row['특징_및_선정_이유']}")
                    if pd.notnull(row['산행코스']):
                        st.write(f"**🗺️ 추천코스:** {row['산행코스']}")
        else:
            st.write("데이터가 없습니다.")

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.info("GitHub에 CSV 파일이 올바른 이름으로 업로드되었는지 확인해주세요.")
