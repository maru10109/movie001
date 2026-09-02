import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

# ==========================================
# [초고퀄리티 렌더링 엔진] 
# 파이썬으로 수백 개의 팝콘 물리/파라볼라 궤적 CSS를 동적으로 생성
# ==========================================
popcorns_html = ""
popcorns_css = ""

# 120개의 팝콘 파티클을 무작위 궤적으로 생성 (CSS 애니메이션)
for i in range(1, 121):
    left_start = random.uniform(10, 15)  # 팝콘통 입구 X 위치 (vw)
    bottom_start = random.uniform(15, 20) # 팝콘통 입구 Y 위치 (vh)
    
    delay = random.uniform(0, 5) # 애니메이션 시작 지연 시간
    duration = random.uniform(1.5, 3.5) # 체공 시간
    
    # 팡팡 터지는 방향과 힘 계산
    x_dist = random.uniform(-300, 400) # 좌우로 퍼지는 거리
    y_dist = random.uniform(300, 800)  # 위로 솟구치는 높이
    rot = random.uniform(360, 1080)    # 회전량
    scale_start = random.uniform(0.4, 0.8)
    scale_peak = random.uniform(1.2, 2.0)
    
    popcorns_html += f'<div class="popcorn p{i}"></div>\n'
    
    # 각 팝콘마다 고유한 CSS 키프레임 할당
    popcorns_css += f"""
    .p{i} {{
        left: {left_start}vw;
        bottom: {bottom_start}vh;
        animation: pop_anim_{i} {duration}s infinite cubic-bezier(0.25, 1, 0.5, 1);
        animation-delay: {delay}s;
    }}
    @keyframes pop_anim_{i} {{
        0% {{ transform: translate(0, 0) scale({scale_start}) rotate(0deg); opacity: 1; filter: brightness(1); }}
        40% {{ transform: translate({x_dist*0.4}px, -{y_dist}px) scale({scale_peak}) rotate({rot*0.5}deg); opacity: 1; filter: brightness(1.2); }}
        100% {{ transform: translate({x_dist}px, -{y_dist*0.1}px) scale({scale_start}) rotate({rot}deg); opacity: 0; filter: brightness(0.5); }}
    }}
    """

# ==========================================
# 극장 상영관 POV 전체 테마 (커튼, 조명, 좌석, 콜라, 팝콘)
# ==========================================
theater_background = f"""
<style>
/* 1. Streamlit 시스템 배경 강제 투명화 (핵심 해결책) */
[data-testid="stAppViewContainer"], .stApp {{
    background-color: transparent !important;
    background: transparent !important;
}}
[data-testid="stHeader"] {{
    background: transparent !important;
}}

/* 2. 메인 컨텐츠 영역(그래프들)을 유리창처럼 반투명하게 띄움 */
.block-container {{
    z-index: 10 !important;
    background: rgba(15, 15, 20, 0.75) !important;
    border-radius: 20px;
    padding: 3rem !important;
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 0 50px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

/* 텍스트 시인성 확보 */
h1, h2, h3, h4, p, span, div {{
    color: #f0f0f5 !important;
}}
.st-info {{
    background-color: rgba(30, 30, 50, 0.8) !important;
    border: 1px solid #5a5a8a !important;
    color: #ffffff !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.5);
}}

/* =======================================
   3. 초고퀄리티 백그라운드 환경 (극장 내부)
   ======================================= */
.theater-pov {{
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -999; /* 제일 뒤로 */
    overflow: hidden;
    pointer-events: none;
    /* 심도 있는 극장 내부 그라데이션 */
    background: radial-gradient(circle at 50% 30%, #2a2a3e 0%, #0a0a10 60%, #000000 100%);
}}

/* 극장 레드 커튼 (좌/우) */
.curtain {{
    position: absolute;
    top: -10%;
    width: 20vw; height: 120vh;
    background: repeating-linear-gradient(to right, #4a0000, #800000 20px, #300000 40px);
    box-shadow: 0 0 30px rgba(0,0,0,0.8);
    filter: drop-shadow(0 0 20px rgba(0,0,0,0.9));
}}
.curtain-left {{
    left: -5vw;
    border-radius: 0 0 50% 0;
    transform: skewY(-10deg);
}}
.curtain-right {{
    right: -5vw;
    border-radius: 0 0 0 50%;
    transform: skewY(10deg);
}}

/* 프로젝터 무빙 라이트 */
.searchlight {{
    position: absolute;
    top: 0; left: 50%;
    width: 150vw; height: 150vh;
    background: conic-gradient(from 180deg at 50% -10%, transparent 40deg, rgba(200, 230, 255, 0.1) 90deg, transparent 140deg);
    transform-origin: 50% -10%;
    animation: sweep 10s infinite alternate ease-in-out;
}}
@keyframes sweep {{
    0% {{ transform: rotate(-15deg); }}
    100% {{ transform: rotate(15deg); }}
}}

/* 극장 의자 실루엣 (좌우) */
.seat {{
    position: absolute;
    bottom: -10vh;
    width: 30vw; height: 40vh;
    background: linear-gradient(to top, #020202, #1a1a24);
    border-radius: 80px 80px 0 0;
    box-shadow: inset 0 20px 50px rgba(255,255,255,0.02), 0 -10px 40px rgba(0,0,0,0.9);
}}
.seat-left {{ left: -10vw; transform: rotate(8deg); }}
.seat-right {{ right: -10vw; transform: rotate(-8deg); }}

/* 콜라 컵 & 입체적인 빨대 */
.cola-cup {{
    position: absolute;
    bottom: 5vh; right: 8vw;
    width: 90px; height: 200px;
    background: linear-gradient(to right, #6b0000 0%, #c11111 40%, #e12222 60%, #5b0000 100%);
    border-radius: 5px 5px 25px 25px;
    transform: perspective(300px) rotateX(15deg) rotateY(-10deg);
    box-shadow: 20px 20px 40px rgba(0,0,0,0.9), inset 8px 0 20px rgba(255,255,255,0.3);
}}
.cola-lid {{
    position: absolute;
    top: -20px; left: -10px; width: 110px; height: 25px;
    background: linear-gradient(to right, #ccc, #fff, #aaa);
    border-radius: 12px;
    box-shadow: 0 8px 15px rgba(0,0,0,0.6);
}}
.straw {{
    position: absolute;
    top: -80px; left: 45px;
    width: 8px; height: 100px;
    background: repeating-linear-gradient(45deg, #fff, #fff 5px, #c11111 5px, #c11111 10px);
    transform: rotate(20deg);
    border-radius: 4px;
    box-shadow: 3px 3px 8px rgba(0,0,0,0.7);
}}

/* 팝콘 통 (클래식 스트라이프) */
.popcorn-bucket {{
    position: absolute;
    bottom: 2vh; left: 10vw;
    width: 160px; height: 220px;
    background: repeating-linear-gradient(to right, #c11111, #c11111 25px, #f4f4f4 25px, #f4f4f4 50px);
    border-radius: 5px 5px 20px 20px;
    transform: perspective(400px) rotateX(10deg) rotateY(15deg);
    box-shadow: -20px 20px 40px rgba(0,0,0,0.9), inset -15px 0 30px rgba(0,0,0,0.4);
}}
.popcorn-bucket::before {{
    content: 'POPCORN';
    position: absolute;
    top: 40%; left: 50%;
    transform: translate(-50%, -50%);
    color: #c11111;
    font-weight: 900;
    font-size: 24px;
    background: white;
    padding: 5px 15px;
    border-radius: 50%;
    border: 3px solid #c11111;
}}

/* 기본 팝콘 조각 베이스 디자인 */
.popcorn {{
    position: absolute;
    width: 40px; height: 40px;
    background: radial-gradient(circle at 30% 30%, #ffffff 20%, #fef5c5 60%, #e0aa26 100%);
    border-radius: 40% 60% 60% 40% / 50% 40% 60% 50%;
    box-shadow: inset -4px -4px 6px rgba(0,0,0,0.2), 4px 4px 8px rgba(0,0,0,0.6);
    opacity: 0;
}}
.popcorn::before, .popcorn::after {{
    content: ''; position: absolute;
    background: radial-gradient(circle at 30% 30%, #ffffff 10%, #fef5c5 70%, #d49520 100%);
    border-radius: 50%;
}}
.popcorn::before {{ width: 22px; height: 22px; top: -6px; left: -6px; }}
.popcorn::after {{ width: 28px; height: 28px; top: 6px; right: -12px; }}

/* 파이썬이 생성한 고유 물리엔진 CSS 주입 */
{popcorns_css}
</style>

<div class="theater-pov">
    <div class="searchlight"></div>
    <div class="curtain curtain-left"></div>
    <div class="curtain curtain-right"></div>
    <div class="seat seat-left"></div>
    <div class="seat seat-right"></div>
    <div class="cola-cup">
        <div class="cola-lid"></div>
        <div class="straw"></div>
    </div>
    <div class="popcorn-bucket"></div>
    <!-- 동적으로 생성된 120개의 팝콘 파티클 -->
    {popcorns_html}
</div>
"""
# HTML/CSS 화면 렌더링
st.markdown(theater_background, unsafe_allow_html=True)

st.title("🍿 극장 관람 모드: 영화 데이터 그래프 도감 2")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0])
    df['movie_count'] = 1 
    
    # 날짜 데이터 전처리 (9번 3D 그래프용)
    df['openDt_date'] = pd.to_datetime(df['openDt'].astype(str), format='%Y%m%d', errors='coerce')
    return df

df = load_data()

# ==========================================
st.header("1. 장르별 영화 편수")
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig1 = px.pie(
    genre_counts, names='genre', values='count', hole=0.4,
)
fig1.update_traces(
    textposition='inside', textinfo='percent+label',
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>'
)
fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig1, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 드라마와 액션 장르가 전체 제작 편수에서 가장 큰 비중을 차지하여, 대중적인 선호도와 배급사의 주력 장르가 무엇인지 명확하게 확인할 수 있습니다.")
st.divider()

# ==========================================
st.header("2. 장르 및 영화별 총 관객 (트리맵)")
fig2 = px.treemap(
    df, path=[px.Constant("전체 영화"), 'genre', 'movieNm'], values='total_audi', color='genre'
)
fig2.update_traces(hovertemplate='<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>')
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig2, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 전체 관객 수 중 특정 장르 내의 소수 메가 히트작들이 박스오피스 파이를 거대하게 차지하는 파레토 법칙을 시각적으로 체감할 수 있습니다.")
st.divider()

# ==========================================
st.header("3. 총 관객 분포 (히스토그램)")
fig3 = px.histogram(df, x='total_audi', nbins=30, labels={'total_audi': '총 관객 수'})
fig3.update_layout(yaxis_title="영화 편수", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig3, use_container_width=True)
max_movie = df.loc[df['total_audi'].idxmax(), 'movieNm']
q3_audi = df['total_audi'].quantile(0.75) 
st.info(f"**💡 이 그래프로 알 수 있는 것:** 대부분의 영화가 관객 수 **{q3_audi:,.0f}명 이하**에 몰려 있으며, **'{max_movie}'**와 같은 소수만이 극단적인 흥행을 달성하는 롱테일 분포입니다.")
st.divider()

# ==========================================
st.header("4. 개봉일 스크린수와 총 관객의 관계 (산점도)")
fig4 = px.scatter(
    df, x='first_scrn', y='total_audi', color='genre', hover_name='movieNm',
    labels={'first_scrn': '개봉일 스크린 수', 'total_audi': '총 관객 수', 'genre': '장르'}
)
fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig4, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 개봉일 스크린 수가 많을수록 총 관객 수가 늘어나는 뚜렷한 양의 상관관계가 나타납니다. 초기 상영관 확보가 흥행의 필수 조건임을 입증합니다.")
st.divider()

# ==========================================
st.header("5. 주요 장르별 총 관객 분포 (상자 그림)")
genre_filter = df['genre'].value_counts()
valid_genres = genre_filter[genre_filter >= 10].index
df_box = df[df['genre'].isin(valid_genres)]

fig5 = px.box(
    df_box, x='genre', y='total_audi', color='genre', hover_name='movieNm',
    points='outliers', labels={'genre': '장르', 'total_audi': '총 관객 수'}
)
fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig5, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 액션, 드라마 같은 주요 장르는 평균도 높지만 상자 위로 튀어 오른 점(초대박 이상치)들이 빈번하여, 텐트폴 영화들이 주로 이 장르에서 탄생합니다.")
st.divider()

# ==========================================
st.header("6. 스크린수, 총 관객, 개봉 첫 주 관객의 관계 (버블 그래프)")
df_bubble = df.copy()
df_bubble['first_week_audi'] = df_bubble['first_week_audi'].clip(lower=0)

fig6 = px.scatter(
    df_bubble, x='first_scrn', y='total_audi', color='genre', size='first_week_audi', 
    hover_name='movieNm', size_max=40,
    labels={'first_scrn': '개봉일 스크린 수', 'total_audi': '총 관객 수', 'genre': '장르', 'first_week_audi': '개봉 첫 주 관객'}
)
fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig6, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 우상단으로 갈수록 원의 크기(첫 주 관객)가 압도적으로 커집니다. 초반 물량 공세와 화제성이 어떻게 흥행 폭발로 이어지는지 보여줍니다.")
st.divider()

# ==========================================
st.header("7. 국가 및 장르별 영화 편수 (선버스트 그래프)")
fig7 = px.sunburst(
    df, path=['nation', 'genre'], values='movie_count', color='nation'
)
fig7.update_traces(hovertemplate='<b>%{label}</b><br>편수: %{value}편<extra></extra>')
fig7.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig7, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 한국 영화는 드라마/범죄에, 미국 영화는 액션/애니메이션에 편중되어 있어 국가별 영화 산업의 타겟 장르 차이를 알 수 있습니다.")
st.divider()

# ==========================================
st.header("🌟 8. 흥행 궤적의 3차원 탐색 (3D 산점도)")
fig8 = px.scatter_3d(
    df_bubble, x='first_scrn', y='first_week_audi', z='days_in_top10', color='genre',
    size='total_audi', hover_name='movieNm',
    labels={
        'first_scrn': '개봉일 스크린수', 
        'first_week_audi': '첫 주 관객수', 
        'days_in_top10': '10위권 생존일',
        'total_audi': '총 관객수(크기)'
    }, opacity=0.8
)
fig8.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis=dict(backgroundcolor="rgba(0,0,0,0)"), yaxis=dict(backgroundcolor="rgba(0,0,0,0)"), zaxis=dict(backgroundcolor="rgba(0,0,0,0)")
    ), height=700
)
st.plotly_chart(fig8, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 마우스로 360도 돌려보세요! 상단으로 솟아있고(장기 상영) 원이 큰 영화들은 개봉 폭발력과 뒷심을 모두 챙긴 전설의 명작들입니다.")
st.divider()

# ==========================================
# 새롭게 추가된 9번째 초고퀄리티 3D 그래프
# ==========================================
st.header("🚀 9. [NEW] 시간 흐름에 따른 장르별 흥행 궤적 (3D 별자리)")

# 시간(개봉일) 순으로 정렬하여 선으로 잇기 위해 데이터 준비
df_time = df.sort_values(by='openDt_date').dropna(subset=['openDt_date'])

fig9 = go.Figure()

# 주요 장르 상위 6개만 추출하여 너무 복잡해지지 않게 처리
top_genres = df_time['genre'].value_counts().head(6).index

for genre in top_genres:
    df_g = df_time[df_time['genre'] == genre]
    
    fig9.add_trace(go.Scatter3d(
        x=df_g['openDt_date'],
        y=df_g['first_scrn'],
        z=df_g['total_audi'],
        mode='lines+markers',
        name=genre,
        marker=dict(
            size=df_g['total_audi'] / max(df_time['total_audi']) * 30 + 5, # 관객수에 비례하는 노드 크기
            color=df_g['total_audi'],
            colorscale='Turbo', # 화려한 색상
            opacity=0.9,
            line=dict(width=1, color='white')
        ),
        line=dict(width=4, color='rgba(255,255,255,0.4)'), # 별자리를 잇는 반투명한 선
        text=df_g['movieNm'],
        hovertemplate=(
            '<b>%{text}</b><br>'
            '개봉일: %{x|%Y-%m-%d}<br>'
            '초기 스크린: %{y:,.0f}개<br>'
            '총 관객수: %{z:,.0f}명'
            '<extra></extra>'
        )
    ))

fig9.update_layout(
    title="시간(X) × 스크린(Y) × 관객수(Z)로 보는 장르별 흥행 별자리 지도",
    scene=dict(
        xaxis_title='개봉 시기 (시간 흐름)',
        yaxis_title='개봉일 확보 스크린 수',
        zaxis_title='최종 총 관객 수',
        xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.2)"),
        yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.2)"),
        zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.2)")
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=800,
    legend=dict(title='장르 (클릭하여 켜기/끄기)', bgcolor='rgba(0,0,0,0.5)', font=dict(color="white"))
)

st.plotly_chart(fig9, use_container_width=True)
st.info("**💡 이 그래프로 알 수 있는 것:** 개봉일을 X축에 배치하여 **영화들이 시간에 따라 어떻게 등장하고 흥행했는지 선(Line)으로 연결**했습니다. 마치 우주의 별자리처럼, 어느 시기에 어떤 장르가 스크린을 장악하고 거대한 관객 수(거대한 구체)를 기록했는지 3D 궤적으로 탐험할 수 있습니다. (우측 범례를 클릭하여 특정 장르만 필터링해 보세요!)")
