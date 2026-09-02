import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

# ==========================================
# 극장 상영관 POV & 팝콘/콜라 고퀄리티 CSS 애니메이션 백그라운드
# ==========================================
theater_background = """
<style>
/* Streamlit 기본 배경 투명화 및 컨테이너 스타일링 */
.stApp {
    background-color: #0b0b10 !important;
}
.main {
    background: rgba(15, 15, 20, 0.85); /* 반투명한 어두운 배경 */
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 0 50px rgba(0, 0, 0, 0.7);
    z-index: 10;
    position: relative;
    backdrop-filter: blur(5px);
}

/* 텍스트 가독성을 위해 흰색 계열로 강제 조정 */
h1, h2, h3, h4, p, span, div {
    color: #f0f0f5 !important;
}
.st-info {
    background-color: rgba(30, 30, 50, 0.7) !important;
    border: 1px solid #4a4a6a !important;
    color: #e0e0e0 !important;
}

/* 백그라운드 극장 효과를 위한 고정 컨테이너 */
.theater-pov {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -999;
    overflow: hidden;
    pointer-events: none;
    background: radial-gradient(circle at 50% -20%, #1a1a2e 0%, #050508 70%);
}

/* 스크린 광원 효과 */
.screen-glow {
    position: absolute;
    top: -10%; left: 50%;
    transform: translateX(-50%);
    width: 80vw; height: 50vh;
    background: radial-gradient(ellipse, rgba(100, 150, 255, 0.15) 0%, transparent 70%);
    animation: flicker 4s infinite alternate;
}
@keyframes flicker {
    0% { opacity: 0.8; }
    50% { opacity: 1; filter: drop-shadow(0 0 30px rgba(100, 150, 255, 0.3)); }
    100% { opacity: 0.9; }
}

/* 극장 의자 실루엣 (좌우) */
.seat {
    position: absolute;
    bottom: -50px;
    width: 25vw; height: 35vh;
    background: linear-gradient(to top, #09090a, #1a0f14);
    border-radius: 50px 50px 0 0;
    box-shadow: inset 0 20px 50px rgba(255,0,0,0.05), 0 -10px 30px rgba(0,0,0,0.9);
}
.seat-left { left: -5vw; transform: rotate(5deg); }
.seat-right { right: -5vw; transform: rotate(-5deg); }

/* 콜라 컵 & 빨대 (우측 하단) */
.cola-cup {
    position: absolute;
    bottom: 2vh; right: 10vw;
    width: 80px; height: 160px;
    background: linear-gradient(to right, #8b0000 0%, #d11111 50%, #8b0000 100%);
    border-radius: 5px 5px 20px 20px;
    transform: perspective(200px) rotateX(10deg);
    box-shadow: 15px 15px 30px rgba(0,0,0,0.8), inset 5px 0 15px rgba(255,255,255,0.2);
}
.cola-cup::before { /* 콜라 뚜껑 */
    content: ''; position: absolute;
    top: -15px; left: -5px; width: 90px; height: 20px;
    background: #eee; border-radius: 10px;
    box-shadow: 0 5px 10px rgba(0,0,0,0.5);
}
.straw {
    position: absolute;
    top: -60px; left: 40px;
    width: 6px; height: 70px;
    background: repeating-linear-gradient(45deg, #fff, #fff 5px, #d11111 5px, #d11111 10px);
    transform: rotate(15deg);
    border-radius: 3px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
}

/* 팝콘 통 (좌측 하단) */
.popcorn-bucket {
    position: absolute;
    bottom: 0; left: 15vw;
    width: 140px; height: 180px;
    background: repeating-linear-gradient(to right, #d11111, #d11111 20px, #fff 20px, #fff 40px);
    border-radius: 5px 5px 15px 15px;
    transform: perspective(300px) rotateX(5deg);
    box-shadow: -15px 15px 30px rgba(0,0,0,0.8), inset -10px 0 20px rgba(0,0,0,0.3);
}

/* 고퀄리티 팝콘 알갱이 및 팡팡 터지는 애니메이션 */
.popcorn-container {
    position: absolute;
    bottom: 160px; left: 16vw;
    width: 120px; height: 10px;
}
.popcorn {
    position: absolute;
    bottom: 0; left: 50%;
    width: 35px; height: 35px;
    background: radial-gradient(circle at 30% 30%, #fff 20%, #fceea7 60%, #e5a32b 100%);
    border-radius: 40% 60% 60% 40% / 50% 40% 60% 50%;
    box-shadow: inset -3px -3px 5px rgba(0,0,0,0.2), 3px 3px 6px rgba(0,0,0,0.5);
    opacity: 0;
}
.popcorn::before, .popcorn::after {
    content: ''; position: absolute;
    background: radial-gradient(circle at 30% 30%, #fff 10%, #fceea7 70%, #d49520 100%);
    border-radius: 50%;
}
.popcorn::before { width: 20px; height: 20px; top: -5px; left: -5px; }
.popcorn::after { width: 25px; height: 25px; top: 5px; right: -10px; }

/* 여러 개의 팝콘 물리/파라볼라 애니메이션 */
@keyframes pop1 {
    0% { transform: translate(0, 0) scale(0.5) rotate(0deg); opacity: 1; }
    40% { transform: translate(-80px, -250px) scale(1.2) rotate(180deg); opacity: 1; }
    100% { transform: translate(-120px, 100px) scale(0.8) rotate(360deg); opacity: 0; }
}
@keyframes pop2 {
    0% { transform: translate(0, 0) scale(0.4) rotate(0deg); opacity: 1; }
    50% { transform: translate(100px, -300px) scale(1.3) rotate(-120deg); opacity: 1; }
    100% { transform: translate(150px, 150px) scale(0.9) rotate(-240deg); opacity: 0; }
}
@keyframes pop3 {
    0% { transform: translate(0, 0) scale(0.6) rotate(0deg); opacity: 1; }
    45% { transform: translate(-30px, -350px) scale(1.5) rotate(200deg); opacity: 1; }
    100% { transform: translate(-50px, 200px) scale(1) rotate(400deg); opacity: 0; }
}
@keyframes pop4 {
    0% { transform: translate(0, 0) scale(0.5) rotate(0deg); opacity: 1; }
    35% { transform: translate(60px, -200px) scale(1.1) rotate(-90deg); opacity: 1; }
    100% { transform: translate(80px, 50px) scale(0.7) rotate(-180deg); opacity: 0; }
}

.p1 { animation: pop1 2.5s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 0.1s; }
.p2 { animation: pop2 3.1s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 0.8s; left: 30%; }
.p3 { animation: pop3 2.8s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 1.5s; left: 70%; }
.p4 { animation: pop4 2.2s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 2.1s; left: 40%; }
.p5 { animation: pop1 3.5s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 0.5s; left: 60%; }
.p6 { animation: pop2 2.7s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 1.2s; left: 20%; }
.p7 { animation: pop3 3.3s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 2.5s; left: 80%; }
.p8 { animation: pop4 2.9s infinite cubic-bezier(0.25, 1, 0.5, 1); animation-delay: 1.8s; left: 50%; }
</style>

<div class="theater-pov">
    <div class="screen-glow"></div>
    <div class="seat seat-left"></div>
    <div class="seat seat-right"></div>
    <div class="cola-cup"><div class="straw"></div></div>
    <div class="popcorn-bucket"></div>
    <div class="popcorn-container">
        <div class="popcorn p1"></div><div class="popcorn p2"></div>
        <div class="popcorn p3"></div><div class="popcorn p4"></div>
        <div class="popcorn p5"></div><div class="popcorn p6"></div>
        <div class="popcorn p7"></div><div class="popcorn p8"></div>
    </div>
</div>
"""
st.markdown(theater_background, unsafe_allow_html=True)

st.title("🍿 영화 데이터 그래프 도감 2 - 분포와 관계")

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
# 다크테마 그래프 투명화
fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig1, use_container_width=True)

st.info("**💡 이 그래프로 알 수 있는 것:** 드라마와 액션 장르가 전체 제작 편수에서 가장 큰 비중을 차지하여, 대중적인 선호도와 배급사의 주력 장르가 무엇인지 명확하게 확인할 수 있습니다.")

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
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig2, use_container_width=True)

st.info("**💡 이 그래프로 알 수 있는 것:** 전체 관객 수 중 액션이나 드라마 장르 내의 '천만 관객'을 돌파한 소수의 메가 히트작들이 박스오피스 전체 점유율을 견인하는 구조(파레토 법칙)를 시각적으로 체감할 수 있습니다.")

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
fig3.update_layout(yaxis_title="영화 편수", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig3, use_container_width=True)

# 시사점 자동 생성 로직
max_movie = df.loc[df['total_audi'].idxmax(), 'movieNm']
q3_audi = df['total_audi'].quantile(0.75) # 상위 25% 기준점

st.info(f"**💡 이 그래프로 알 수 있는 것:** 대부분의 영화가 관객 수 **{q3_audi:,.0f}명 이하**의 하위 구간에 몰려 있으며, **'{max_movie}'**와 같은 소수의 영화만이 극단적으로 높은 관객 수를 달성하는 '롱테일(Long Tail)' 분포를 보여줍니다.")

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
fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig4, use_container_width=True)

st.info("**💡 이 그래프로 알 수 있는 것:** 개봉일 스크린 수가 많을수록 총 관객 수가 늘어나는 뚜렷한 우상향(양의 상관관계) 패턴을 보여주며, 이는 초기 상영관 확보가 흥행의 핵심 필수 요인임을 입증합니다.")

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
fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig5, use_container_width=True)

st.info("**💡 이 그래프로 알 수 있는 것:** 주요 장르(액션, 드라마)는 평균 관객 수도 높지만 꼬리표처럼 상자 위로 높게 튀어 오른 점(이상치)들이 빈번하여, 대박을 터뜨리는 흥행작이 주로 이 장르들에서 탄생함을 알 수 있습니다.")

st.divider()

# ==========================================
# ==========================================
st.header("6. 스크린수, 총 관객, 개봉 첫 주 관객의 관계 (버블 그래프)")

# 버블 크기에 음수가 들어가는 것을 방지
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
fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig6, use_container_width=True)

st.info("**💡 이 그래프로 알 수 있는 것:** 우상단에 위치할수록 원의 크기(첫 주 관객)가 압도적으로 커집니다. 즉, 많은 스크린 수와 초반 폭발적인 화제성이 결합될 때 엄청난 최종 흥행으로 직결되는 블록버스터의 공식을 보여줍니다.")

st.divider()

# ==========================================
# ==========================================
st.header("7. 국가 및 장르별 영화 편수 (선버스트 그래프)")

fig7 = px.sunburst(
    df,
    path=['nation', 'genre'],
    values='movie_count',
    color='nation'
)
fig7.update_traces(hovertemplate='<b>%{label}</b><br>편수: %{value}편<extra></extra>')
fig7.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig7, use_container_width=True)

st.info("**💡 이 그래프로 알 수 있는 것:** 한국 영화는 '드라마'와 '범죄/코미디' 장르에, 미국 영화는 '액션'과 '애니메이션' 장르에 편중되어 있어, 국가별 영화 산업이 주력하고 관객이 기대하는 장르적 특징이 다름을 확인할 수 있습니다.")

st.divider()

# ==========================================
# ==========================================
st.header("🌟 8. 흥행 궤적의 3차원 탐색 (3D 산점도)")

# 새로 추가된 신기한 그래프 (3D Scatter)
fig8 = px.scatter_3d(
    df_bubble,
    x='first_scrn',
    y='first_week_audi',
    z='days_in_top10',
    color='genre',
    size='total_audi',
    hover_name='movieNm',
    labels={
        'first_scrn': '개봉일 스크린수', 
        'first_week_audi': '첫 주 관객수', 
        'days_in_top10': '10위권 생존일(일)',
        'total_audi': '총 관객수(원 크기)'
    },
    opacity=0.7
)

# 3D 차트 배경 어둡게 설정
fig8.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
        yaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
        zaxis=dict(backgroundcolor="rgba(0,0,0,0)")
    ),
    height=700
)

st.plotly_chart(fig8, use_container_width=True)

st.info("**💡 이 그래프로 알 수 있는 것:** X축(초기 스크린), Y축(초반 화제성), Z축(장기 흥행력)을 동시에 360도로 돌려보며 분석할 수 있습니다. 상단으로 높이 솟아 있으면서 원의 크기가 큰 영화들은 '개봉 초기 폭발력 + 장기 흥행' 두 마리 토끼를 모두 잡은 전설적인 명작들입니다. (마우스를 드래그하여 회전시켜 보세요!)")
