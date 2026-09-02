import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리: 여러 장르가 있을 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0])
    # 편수 계산을 위한 임시 컬럼 추가
    df['movie_count'] = 1 
    return df

df = load_data()

# ==========================================
# ==========================================
st.header("1. 장르별 영화 편수")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig1 = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
)
fig1.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>'
)
st.plotly_chart(fig1, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** [이곳에 장르 분포에 대한 한 줄 요약을 입력하세요]")

st.divider()

# ==========================================
# ==========================================
st.header("2. 장르 및 영화별 총 관객 (트리맵)")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre'
)
fig2.update_traces(hovertemplate='<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>')

st.plotly_chart(fig2, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** [이곳에 관객 수가 많은 장르나 영화에 대한 한 줄 요약을 입력하세요]")

st.divider()

# ==========================================
# ==========================================
st.header("3. 총 관객 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    labels={'total_audi': '총 관객 수'}
)
fig3.update_layout(yaxis_title="영화 편수")

st.plotly_chart(fig3, use_container_width=True)

# 시사점 자동 생성 로직
max_movie = df.loc[df['total_audi'].idxmax(), 'movieNm']
q3_audi = df['total_audi'].quantile(0.75) # 상위 25% 기준점

st.info(f"**💡 이 그래프로 알 수 있는 것:** 대부분의 영화가 관객 수 **{q3_audi:,.0f}명 이하** 구간에 몰려 있으며, 가장 관객이 많은 영화는 **'{max_movie}'**입니다.")

st.divider()

# ==========================================
# ==========================================
st.header("4. 개봉일 스크린수와 총 관객의 관계 (산점도)")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    labels={'first_scrn': '개봉일 스크린 수', 'total_audi': '총 관객 수', 'genre': '장르'}
)

st.plotly_chart(fig4, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** [이곳에 스크린 수와 관객 수의 비례 관계 등에 대한 한 줄 요약을 입력하세요]")

st.divider()

# ==========================================
# ==========================================
st.header("5. 주요 장르별 총 관객 분포 (상자 그림)")

# 영화가 10편 이상인 장르만 필터링
genre_filter = df['genre'].value_counts()
valid_genres = genre_filter[genre_filter >= 10].index
df_box = df[df['genre'].isin(valid_genres)]

fig5 = px.box(
    df_box,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points='outliers', # 이상치 점 표시
    labels={'genre': '장르', 'total_audi': '총 관객 수'}
)

st.plotly_chart(fig5, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** [이곳에 장르별 관객 수의 편차나 이상치(대박 영화)에 대한 한 줄 요약을 입력하세요]")

st.divider()

# ==========================================
# ==========================================
st.header("6. 스크린수, 총 관객, 개봉 첫 주 관객의 관계 (버블 그래프)")

# 버블 크기에 음수가 들어가는 것을 방지 (결측치나 이상치 대비)
df_bubble = df.copy()
df_bubble['first_week_audi'] = df_bubble['first_week_audi'].clip(lower=0)

fig6 = px.scatter(
    df_bubble,
    x='first_scrn',
    y='total_audi',
    color='genre',
    size='first_week_audi', # 버블 크기
    hover_name='movieNm',
    size_max=40,
    labels={'first_scrn': '개봉일 스크린 수', 'total_audi': '총 관객 수', 'genre': '장르', 'first_week_audi': '개봉 첫 주 관객'}
)

st.plotly_chart(fig6, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** [이곳에 원의 크기(첫 주 관객)가 총 관객 수에 미치는 영향 등에 대한 한 줄 요약을 입력하세요]")

st.divider()

# ==========================================
# ==========================================
st.header("7. 국가 및 장르별 영화 편수 (선버스트 그래프)")

fig7 = px.sunburst(
    df,
    path=['nation', 'genre'],
    values='movie_count', # 편수 기준 크기 할당
    color='nation'
)
fig7.update_traces(hovertemplate='<b>%{label}</b><br>편수: %{value}편<extra></extra>')

st.plotly_chart(fig7, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** [이곳에 국가별로 선호/제작되는 주요 장르 분포에 대한 한 줄 요약을 입력하세요]")
