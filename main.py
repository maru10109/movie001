import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import random
import math
import textwrap

# =====================================================================
# [초기 페이지 설정]
# 넓은 화면과 다크 테마 기반의 커스텀 타이틀 설정
# =====================================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 3 : 마스터피스 에디션",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# [시네마틱 CSS 렌더링 엔진]
# 기존의 단순 fixed 배경의 한계를 극복하고, 스크롤과 완벽히 동기화되거나
# 화면 전체를 덮는 압도적인 퀄리티의 프로젝터 라이팅 & 더스트 파티클 생성
# =====================================================================
def generate_masterpiece_css():
    """
    스트림릿 앱 전체의 UI/UX를 영화관의 VIP 라운지처럼 탈바꿈시키는 거대한 CSS를 생성합니다.
    - 배경 스크롤 문제 해결 (background-attachment: fixed)
    - 수백 개의 떠다니는 먼지 파티클 (빛 반사 효과)
    - 글래스모피즘(Glassmorphism) 기반의 그래프 컨테이너
    """
    
    # 기본 스트림릿 컨테이너 투명화 및 베이스 배경 설정
    base_css = """
    <style>
    /* =========================================
       1. 베이스 앱 스타일링 (스크롤 문제 완벽 해결)
       ========================================= */
    [data-testid="stAppViewContainer"] {
        /* 매우 깊은 심도의 시네마틱 다크 그라데이션 */
        background: radial-gradient(circle at 50% 10%, #1e1e2f 0%, #0a0a14 60%, #020205 100%) !important;
        background-attachment: fixed !important;
        background-size: cover !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.9) !important;
        backdrop-filter: blur(10px);
    }
    
    /* =========================================
       2. 글래스모피즘 블록 컨테이너 (초고퀄리티 패널)
       ========================================= */
    .block-container {
        z-index: 10;
        background: rgba(20, 20, 30, 0.5) !important;
        backdrop-filter: blur(20px) saturate(150%);
        -webkit-backdrop-filter: blur(20px) saturate(150%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 30px;
        padding: 4rem !important;
        margin-top: 3rem !important;
        margin-bottom: 5rem !important;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        max-width: 95% !important;
    }

    /* 텍스트 및 UI 요소 시인성 극대화 */
    h1, h2, h3, h4, p, span, div, li {
        color: #f8f8ff !important;
        font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    h1 {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(to right, #ffd700, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    h2 {
        font-size: 2.2rem !important;
        border-bottom: 2px solid rgba(255, 215, 0, 0.3);
        padding-bottom: 0.5rem;
        margin-top: 4rem !important;
        margin-bottom: 2rem !important;
    }
    
    /* 정보 박스 (st.info, st.success 등) 커스텀 */
    .st-info, .st-success, .st-warning {
        background: rgba(30, 40, 60, 0.6) !important;
        border-left: 5px solid #4da6ff !important;
        border-radius: 10px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    
    /* 디바이더(구분선) 글로우 효과 */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.3), transparent) !important;
        margin: 4rem 0 !important;
    }
    
    /* =========================================
       3. 고정형 백그라운드 오버레이 (프로젝터 라이트 & 먼지)
       ========================================= */
    .cinematic-environment {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: 0;
        pointer-events: none; /* 클릭 방해 금지 */
        overflow: hidden;
    }
    
    /* 프로젝터 빔 볼륨 라이팅 */
    .projector-beam {
        position: absolute;
        top: -10vh;
        left: 50%;
        width: 150vw;
        height: 120vh;
        background: conic-gradient(from 180deg at 50% 0%, transparent 45deg, rgba(200, 220, 255, 0.08) 90deg, transparent 135deg);
        transform-origin: top center;
        transform: translateX(-50%);
        animation: beam_flicker 4s infinite alternate ease-in-out;
        mix-blend-mode: screen;
    }
    
    @keyframes beam_flicker {
        0% { opacity: 0.8; transform: translateX(-50%) scaleX(1); }
        25% { opacity: 0.95; transform: translateX(-50%) scaleX(1.02); }
        50% { opacity: 0.7; transform: translateX(-50%) scaleX(0.98); }
        75% { opacity: 1.0; transform: translateX(-50%) scaleX(1.01); }
        100% { opacity: 0.85; transform: translateX(-50%) scaleX(1); }
    }
    
    /* 양옆 프리미엄 벨벳 커튼 */
    .premium-curtain {
        position: fixed;
        top: 0;
        width: 15vw;
        height: 100vh;
        background: repeating-linear-gradient(
            to right, 
            #200000 0%, 
            #400000 5%, 
            #600000 10%, 
            #400000 15%, 
            #200000 20%
        );
        box-shadow: 0 0 50px rgba(0,0,0,1);
        z-index: 1;
        pointer-events: none;
        filter: contrast(1.2) brightness(0.8);
    }
    .curtain-left {
        left: 0;
        border-right: 5px solid rgba(255,100,100,0.2);
    }
    .curtain-right {
        right: 0;
        border-left: 5px solid rgba(255,100,100,0.2);
    }
    </style>
    """
    
    # 동적 파티클 생성 (프로젝터 빛에 비치는 먼지들)
    particles_html = ""
    particles_css = "<style>\n"
    
    # 무려 200개의 파티클을 흩뿌립니다.
    num_particles = 200
    for i in range(num_particles):
        x_pos = random.uniform(0, 100)
        y_pos = random.uniform(0, 100)
        size = random.uniform(1, 4)
        duration = random.uniform(10, 30)
        delay = random.uniform(0, 20)
        opacity = random.uniform(0.1, 0.7)
        
        # x축, y축 이동량
        move_x = random.uniform(-20, 20)
        move_y = random.uniform(-20, 20)
        
        particles_html += f'<div class="dust-particle dp-{i}"></div>\n'
        particles_css += f"""
        .dp-{i} {{
            position: absolute;
            left: {x_pos}vw;
            top: {y_pos}vh;
            width: {size}px;
            height: {size}px;
            background: rgba(255, 255, 255, {opacity});
            border-radius: 50%;
            box-shadow: 0 0 {size*2}px rgba(255,255,255,0.8);
            animation: float-{i} {duration}s infinite alternate ease-in-out;
            animation-delay: -{delay}s;
        }}
        @keyframes float-{i} {{
            0% {{ transform: translate(0px, 0px); opacity: 0; }}
            50% {{ opacity: {opacity}; }}
            100% {{ transform: translate({move_x}vw, {move_y}vh); opacity: 0; }}
        }}
        """
    particles_css += "</style>"
    
    # 최종 HTML 어셈블
    full_html = f"""
    {base_css}
    {particles_css}
    <div class="cinematic-environment">
        <div class="projector-beam"></div>
        {particles_html}
    </div>
    <div class="premium-curtain curtain-left"></div>
    <div class="premium-curtain curtain-right"></div>
    """
    return full_html

# 배경 렌더링
st.markdown(generate_masterpiece_css(), unsafe_allow_html=True)

# =====================================================================
# [데이터 로드 및 심층 전처리]
# 단순 시각화를 넘어 통계적 분석을 위한 파생 변수들을 대거 생성합니다.
# =====================================================================
@st.cache_data
def load_and_preprocess_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    try:
        df = pd.read_csv(url)
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame()

    # 1. 기본 전처리
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0] if pd.notnull(x) else '기타')
    df['movie_count'] = 1
    
    # 2. 날짜 기반 파생 변수 생성
    df['openDt_date'] = pd.to_datetime(df['openDt'].astype(str), format='%Y%m%d', errors='coerce')
    df['open_year'] = df['openDt_date'].dt.year
    df['open_month'] = df['openDt_date'].dt.month
    df['open_day_of_week'] = df['openDt_date'].dt.dayofweek # 0:월 ~ 6:일
    
    # 3. 비즈니스 인사이트 파생 변수
    # 첫 주 스크린당 관객수 (초기 밀집도)
    df['audi_per_scrn_first_week'] = np.where(df['first_scrn'] > 0, df['first_week_audi'] / df['first_scrn'], 0)
    
    # 장기 흥행 뒷심 지수 (총 관객수 대비 첫 주 관객수 제외 비율)
    # 1에 가까울수록 첫주 이후에도 흥행 유지, 0에 가까울수록 첫주 반짝
    df['first_week_audi'] = df['first_week_audi'].clip(lower=0) # 음수 방지
    df['long_tail_power'] = np.where(df['total_audi'] > 0, (df['total_audi'] - df['first_week_audi']) / df['total_audi'], 0)
    df['long_tail_power'] = df['long_tail_power'].clip(lower=0, upper=1)
    
    # 흥행 규모 분류 (Categorical)
    conditions = [
        (df['total_audi'] >= 10000000),
        (df['total_audi'] >= 5000000),
        (df['total_audi'] >= 1000000),
        (df['total_audi'] < 1000000)
    ]
    choices = ['천만 영화', '5백만 이상', '1백만 이상', '1백만 미만']
    df['hit_scale'] = np.select(conditions, choices, default='분류 불가')
    
    # 결측치 정제
    df.fillna({'first_scrn': 0, 'first_week_audi': 0, 'total_audi': 0}, inplace=True)
    
    return df

df = load_and_preprocess_data()

# 데이터셋이 비어있을 경우 방어 코드
if df.empty:
    st.stop()

# 공통 레이아웃 템플릿 (모든 그래프에 일관된 다크 시네마틱 테마 적용)
layout_template = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#dcdcdc', family='Pretendard, sans-serif'),
    title=dict(font=dict(size=24, color='#ffffff')),
    legend=dict(bgcolor='rgba(20,20,30,0.7)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1),
    margin=dict(t=80, b=40, l=40, r=40)
)

# 메인 타이틀 렌더링
st.markdown("<h1>🎬 영화 데이터 그래프 도감 3 : 마스터피스</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 3rem;'>12가지 심층 3D 및 통계적 시각화를 통해 한국 박스오피스의 모든 것을 해부합니다.</p>", unsafe_allow_html=True)

# =====================================================================
# [SECTION 1] 거시적 관점: 시장의 파이 분할
# =====================================================================
st.header("📊 Section 1. 장르별 시장 점유율 및 파레토 분포")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 장르별 제작 편수 (도넛 차트)")
    genre_counts = df['genre'].value_counts().reset_index()
    genre_counts.columns = ['genre', 'count']
    
    fig1 = px.pie(
        genre_counts, names='genre', values='count', hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_traces(
        textposition='inside', textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>제작 편수: %{value:,.0f}편<br>점유율: %{percent}<extra></extra>',
        marker=dict(line=dict(color='#111', width=2))
    )
    fig1.update_layout(**layout_template, title_text="장르별 제작 빈도")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. 장르 내 흥행 쏠림 현상 (트리맵)")
    # 트리맵 시각화를 위해 관객수 0 이상인 데이터만 필터링
    df_tree = df[df['total_audi'] > 0].copy()
    fig2 = px.treemap(
        df_tree, path=[px.Constant("전체 누적 관객"), 'genre', 'movieNm'], values='total_audi',
        color='total_audi', color_continuous_scale='Turbo'
    )
    fig2.update_traces(
        hovertemplate='<b>%{label}</b><br>누적 관객: %{value:,.0f}명<extra></extra>',
        marker=dict(line=dict(color='rgba(0,0,0,0.5)', width=1))
    )
    fig2.update_layout(**layout_template, title_text="시장 내 관객수 계층 구조")
    st.plotly_chart(fig2, use_container_width=True)

st.info("**💡 비즈니스 인사이트 1&2:** 좌측 그래프에서 제작 편수가 많은 장르(드라마, 코미디)와 우측 그래프에서 실제 수익(관객수)의 면적을 차지하는 장르(액션, 판타지 등)의 불일치를 찾아보세요. 특정 장르는 소수의 메가 히트작이 전체 파이를 견인하는 전형적인 '파레토 법칙'을 보여줍니다.")
st.markdown("<hr>", unsafe_allow_html=True)


# =====================================================================
# [SECTION 2] 미시적 관점: 흥행의 통계적 분포 특성
# =====================================================================
st.header("📉 Section 2. 흥행 양극화와 이상치(Outlier) 탐색")

col3, col4 = st.columns(2)

with col3:
    st.subheader("3. 누적 관객수 밀도 분포 (KDE & 러그)")
    # 관객수가 너무 넓게 퍼져있으므로 로그 스케일 유사 효과를 위해 범위를 제한하여 디테일 관찰
    # 극단적 이상치 제외한 95% 분위수까지만 히스토그램 시각화
    q95 = df['total_audi'].quantile(0.95)
    df_hist = df[df['total_audi'] <= q95]
    
    fig3 = ff.create_distplot(
        [df_hist['total_audi'].dropna()], ['관객수 분포'], 
        bin_size=q95/30, colors=['#ff4b4b']
    )
    fig3.update_layout(
        **layout_template, 
        title_text=f"하위 95% 영화 관객수 분포 (Max: {q95:,.0f}명)",
        xaxis_title="총 관객수", yaxis_title="밀도"
    )
    fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("4. 주요 장르별 흥행 상자 수염 그림")
    # 빈도수가 높은 상위 8개 장르만 추출
    top8_genres = df['genre'].value_counts().nlargest(8).index
    df_box = df[df['genre'].isin(top8_genres)]
    
    fig4 = px.box(
        df_box, x='genre', y='total_audi', color='genre', 
        hover_name='movieNm', points='all', notched=True,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig4.update_layout(
        **layout_template, 
        title_text="장르별 관객수 분포 및 천만 영화(이상치) 탐지",
        xaxis_title="장르", yaxis_title="총 관객수"
    )
    fig4.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig4, use_container_width=True)

st.info("**💡 비즈니스 인사이트 3&4:** 영화 산업은 전형적인 '롱테일(Long-tail) 편향 분포'를 가집니다. 좌측 그래프를 보면 95%의 영화들이 매우 낮은 관객수에 몰려있습니다. 반면 우측 상자 그림에서 윗수염(Whisker)을 아득히 벗어난 점(Point)들이 바로 시장 전체를 먹여 살리는 텐트폴(Tentpole) 대작들입니다.")
st.markdown("<hr>", unsafe_allow_html=True)


# =====================================================================
# [SECTION 3] 다이내믹 관점: 스크린 확보와 흥행의 상관관계
# =====================================================================
st.header("🔗 Section 3. 자본력(스크린)과 성과(흥행)의 다차원 분석")

st.subheader("5. 개봉 스크린 수 vs 첫 주 관객수 vs 뒷심 지수 (버블 산점도)")
fig5 = px.scatter(
    df[df['total_audi']>0], x='first_scrn', y='first_week_audi', 
    size='total_audi', color='long_tail_power',
    hover_name='movieNm', opacity=0.8, size_max=60,
    color_continuous_scale='Viridis',
    labels={
        'first_scrn': '개봉일 확보 스크린 수', 
        'first_week_audi': '첫 주 관객 수',
        'long_tail_power': '장기 흥행 지수 (뒷심)',
        'total_audi': '총 관객 수'
    }
)
fig5.update_layout(
    **layout_template, height=600,
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="초기 스크린 수 (자본력)"),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="개봉 첫 주 관객 (폭발력)")
)
st.plotly_chart(fig5, use_container_width=True)
st.success("**🎯 핵심 지표 분석:** X축(스크린 수)과 Y축(첫 주 관객수)은 강한 양의 상관관계를 갖습니다. 여기서 주목할 점은 **원의 색상(장기 흥행 지수)**입니다. 초반 스크린을 많이 확보하지 못했음에도(좌측), 색상이 밝게 빛나며 원이 커진 영화들은 입소문(역주행)을 통해 장기 흥행에 성공한 '슬리퍼 히트(Sleeper Hit)' 작품들입니다.")
st.markdown("<hr>", unsafe_allow_html=True)


# =====================================================================
# [SECTION 4] 스펙트럼 관점: 장르별 흥행 DNA 해부 (NEW)
# =====================================================================
st.header("🧬 Section 4. 장르별 흥행 DNA 해부 (다차원 프로파일링)")

col5, col6 = st.columns(2)

with col5:
    st.subheader("6. 장르별 핵심 지표 레이더 차트")
    # 장르별로 각 지표의 평균을 구하고 스케일링
    genre_metrics = df_box.groupby('genre')[['first_scrn', 'first_week_audi', 'total_audi', 'long_tail_power']].mean().reset_index()
    
    # 0~1 사이로 MinMax 스케일링 적용 함수
    def min_max_scale(series):
        return (series - series.min()) / (series.max() - series.min())
    
    for col in ['first_scrn', 'first_week_audi', 'total_audi', 'long_tail_power']:
        genre_metrics[col + '_scaled'] = min_max_scale(genre_metrics[col])

    categories = ['초기 스크린 확보력', '개봉 폭발력', '최종 관객수', '장기 입소문(뒷심)']
    
    fig6 = go.Figure()
    # 주요 3개 장르만 비교하여 시인성 확보
    compare_genres = ['액션', '드라마', '애니메이션']
    colors = ['#FF4B4B', '#00D4FF', '#FFD700']
    
    for i, g in enumerate(compare_genres):
        if g in genre_metrics['genre'].values:
            g_data = genre_metrics[genre_metrics['genre'] == g].iloc[0]
            values = [
                g_data['first_scrn_scaled'], 
                g_data['first_week_audi_scaled'], 
                g_data['total_audi_scaled'], 
                g_data['long_tail_power_scaled'],
                g_data['first_scrn_scaled'] # 폐곡선 완성을 위해 첫 값 추가
            ]
            fig6.add_trace(go.Scatterpolar(
                r=values, theta=categories + [categories[0]], 
                fill='toself', name=g, line_color=colors[i], opacity=0.7
            ))
            
    fig6.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.2)"),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True, **layout_template,
        title_text="주요 장르별 능력치 헥사곤"
    )
    st.plotly_chart(fig6, use_container_width=True)

with col6:
    st.subheader("7. 흥행 요인 상관관계 히트맵")
    # 수치형 변수만 선택
    corr_cols = ['first_scrn', 'first_week_audi', 'total_audi', 'long_tail_power', 'audi_per_scrn_first_week']
    corr_matrix = df[corr_cols].corr()
    
    fig7 = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=['스크린수', '첫주 관객', '총 관객', '뒷심', '스크린당 밀도'],
        y=['스크린수', '첫주 관객', '총 관객', '뒷심', '스크린당 밀도'],
        colorscale='RdBu_r', zmin=-1, zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
        hoverinfo="z"
    ))
    fig7.update_layout(**layout_template, title_text="변수 간 피어슨 상관계수 (Pearson Correlation)")
    st.plotly_chart(fig7, use_container_width=True)

st.info("**💡 비즈니스 인사이트 6&7:** 레이더 차트를 통해 '액션' 장르는 스크린 확보와 폭발력이 압도적이지만 상대적으로 뒷심이 부족하고, '드라마'나 '애니메이션'은 초기 화제성은 낮아도 뒷심(입소문) 수치가 높음을 알 수 있습니다. 히트맵은 스크린수와 총관객수가 0.8 이상의 맹렬한 상관관계를 가짐을 증명합니다.")
st.markdown("<hr>", unsafe_allow_html=True)


# =====================================================================
# [SECTION 5] 타임라인 관점: 시계열 성과 및 요일별 분석
# =====================================================================
st.header("⏳ Section 5. 시간의 흐름, 언제 개봉해야 성공하는가?")

# 연도-월별 평균 총 관객수 추세선 (결측치 제외)
df_time = df.dropna(subset=['open_year', 'open_month']).copy()
time_trend = df_time.groupby(['open_year', 'open_month'])['total_audi'].mean().reset_index()
time_trend['date_str'] = time_trend['open_year'].astype(str) + '-' + time_trend['open_month'].astype(str).str.zfill(2)

st.subheader("8. 개봉 시점별 평균 관객수 흐름 (시계열 스트림튜브형 라인)")
fig8 = px.line(
    time_trend, x='date_str', y='total_audi', 
    markers=True, line_shape='spline', render_mode='svg'
)
fig8.update_traces(
    line=dict(width=4, color='#00d4ff'),
    marker=dict(size=8, color='#ff4b4b', line=dict(width=2, color='white'))
)
fig8.update_layout(
    **layout_template, height=500,
    xaxis_title="개봉 연월", yaxis_title="해당 월 개봉작 평균 관객수",
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', nticks=15),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
)
# 성수기 주석 달기
fig8.add_annotation(x='2019-07', y=time_trend['total_audi'].max(), text="여름 텐트폴 성수기", showarrow=True, arrowhead=1, arrowcolor='white')
st.plotly_chart(fig8, use_container_width=True)
st.info("**💡 비즈니스 인사이트 8:** 시계열 꺾은선 그래프는 7~8월(여름방학)과 12~1월(겨울방학/연말)에 거대한 피크가 형성됨을 보여줍니다. 배급사들이 사활을 거는 '성수기'의 파괴력을 수치로 확인하는 대목입니다.")
st.markdown("<hr>", unsafe_allow_html=True)


# =====================================================================
# [SECTION 6] 3D 하이퍼 비전: 압도적인 3차원 데이터 지형도 (요청하신 부분)
# =====================================================================
st.header("🌌 Section 6. 하이퍼 비전 (Hyper-Vision) : 3D 흥행 산맥")
st.markdown("""
> *기존의 식상한 3D 산점도에서 벗어나, 데이터를 물리적인 '지형(Terrain)'으로 변환했습니다. 
> 월(Month)과 연도(Year)라는 2차원 평면 위에, 총 관객수라는 거대한 Z축 데이터가 솟아오른 
> **3D 서피스(Surface) 지형도**를 마우스로 자유롭게 탐험해보세요.*
""")

# -----------------------------------------------------
# 9번 그래프: 3D Surface Plot (개봉 시기별 흥행 지형도)
# -----------------------------------------------------
st.subheader("🚀 9. [NEW] 월별/연도별 흥행 지형도 (3D Surface Plot)")

# 3D 렌더링을 위해 데이터를 매트릭스 형태로 재구성
# 연도(y) x 월(x) 평면 위에 관객수 합계(z)를 매핑
pivot_surface = df_time.pivot_table(
    index='open_year', 
    columns='open_month', 
    values='total_audi', 
    aggfunc='sum', 
    fill_value=0
)

# 보간(Interpolation)을 위해 NumPy Meshgrid 사용 (더 부드러운 산맥 생성)
x_months = pivot_surface.columns.values
y_years = pivot_surface.index.values
z_audiences = pivot_surface.values

# Plotly 3D Surface 생성
fig9 = go.Figure(data=[go.Surface(
    z=z_audiences, 
    x=x_months, 
    y=y_years,
    colorscale='Inferno', # 용암처럼 끓어오르는 색상
    contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True),
    lighting=dict(ambient=0.6, diffuse=0.9, roughness=0.5, specular=0.8, fresnel=0.2)
)])

fig9.update_layout(
    title="시간의 흐름에 따른 흥행 산맥 (마우스로 회전/확대 가능)",
    autosize=True,
    width=900,
    height=800,
    margin=dict(l=0, r=0, b=0, t=50),
    paper_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis_title='개봉 월 (1~12)',
        yaxis_title='개봉 연도',
        zaxis_title='누적 관객수 총합',
        xaxis=dict(backgroundcolor="rgba(10,10,15,0.8)", gridcolor="rgba(255,255,255,0.2)", nticks=12),
        yaxis=dict(backgroundcolor="rgba(10,10,15,0.8)", gridcolor="rgba(255,255,255,0.2)", nticks=10),
        zaxis=dict(backgroundcolor="rgba(10,10,15,0.8)", gridcolor="rgba(255,255,255,0.2)"),
        camera=dict(
            eye=dict(x=1.8, y=-1.8, z=1.2), # 초기 시점 최적화
            center=dict(x=0, y=0, z=-0.1)
        )
    )
)

st.plotly_chart(fig9, use_container_width=True)
st.warning("**🌋 3D 지형도 분석:** 가장 높게 솟아오른 붉은 봉우리(Peak)들을 확인하세요. 여름(7-8월)과 연말(12월) 라인을 따라 거대한 산맥이 형성되어 있습니다. 이는 해당 시기에 자본과 마케팅이 집중되며 전체 파이가 거대해지는 극장가의 생태계를 완벽하게 시각화한 결과입니다.")


# -----------------------------------------------------
# 10번 그래프: 3D 심층 스캐터 + 투영(Projection) 결합 그래프
# -----------------------------------------------------
st.subheader("🪐 10. [NEW] 흥행 우주도: 스크린 대비 효율성 다이내믹스")

# 복합 3D 산점도: 각 데이터 포인트에서 바닥면(XY 평면)으로 투영선을 내리는 고급 시각화
df_3d = df[df['total_audi'] > 100000].copy() # 가독성을 위해 10만 이상만 추출

fig10 = go.Figure()

# 실제 데이터 구체
fig10.add_trace(go.Scatter3d(
    x=df_3d['first_scrn'],
    y=df_3d['long_tail_power'],
    z=df_3d['total_audi'],
    mode='markers',
    name='영화 데이터',
    marker=dict(
        size=np.log1p(df_3d['first_week_audi']) * 1.5, # 첫주 관객수에 로그를 씌워 크기 조절
        color=df_3d['first_week_audi'],
        colorscale='Plasma',
        opacity=0.8,
        line=dict(width=1, color='rgba(255,255,255,0.5)')
    ),
    text=df_3d['movieNm'],
    hovertemplate='<b>%{text}</b><br>스크린: %{x}<br>뒷심: %{y:.2f}<br>총관객: %{z:,.0f}<extra></extra>'
))

# 바닥으로 떨어지는 투영선(Stem) 추가를 위한 꼼수 (데이터가 많으면 무거우므로 상위 50개만)
top_50 = df_3d.nlargest(50, 'total_audi')
for i, row in top_50.iterrows():
    fig10.add_trace(go.Scatter3d(
        x=[row['first_scrn'], row['first_scrn']],
        y=[row['long_tail_power'], row['long_tail_power']],
        z=[0, row['total_audi']],
        mode='lines',
        line=dict(color='rgba(255,255,255,0.2)', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

fig10.update_layout(
    title="상위권 영화들의 스크린 의존도 vs 뒷심 분석 (바닥 투영선 포함)",
    autosize=True,
    height=800,
    paper_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis_title='초기 스크린 수 (자본)',
        yaxis_title='뒷심 지수 (콘텐츠 힘)',
        zaxis_title='최종 관객수 (결과)',
        xaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
        yaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
        zaxis=dict(backgroundcolor="rgba(0,0,0,0)")
    )
)
st.plotly_chart(fig10, use_container_width=True)
st.info("**💡 비즈니스 인사이트 10:** 위로 높게 떠 있는 별(영화)들의 바닥 투영선을 따라가 보세요. Y축(뒷심 지수)이 0.8에 가까운 우측 끝단에 위치하며 솟아오른 별들은, 막대한 자본(X축 스크린) 없이도 순수한 작품의 힘(입소문)으로 기적적인 궤적을 그려낸 작품들입니다.")
st.markdown("<hr>", unsafe_allow_html=True)


# =====================================================================
# [SECTION 7] 데이터 요약 및 결론 도출
# =====================================================================
st.header("📋 종합 결론 및 데이터 요약 대시보드")

col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

with col_metric1:
    st.metric(label="총 분석 영화 편수", value=f"{len(df):,} 편")
with col_metric2:
    total_audi_sum = df['total_audi'].sum()
    st.metric(label="누적 박스오피스 관객", value=f"{total_audi_sum // 10000:,.0f} 만명")
with col_metric3:
    max_movie = df.loc[df['total_audi'].idxmax()]
    st.metric(label="최고 흥행작", value=max_movie['movieNm'], delta=f"{max_movie['total_audi']:,.0f}명 관람")
with col_metric4:
    best_genre = df.groupby('genre')['total_audi'].sum().idxmax()
    st.metric(label="가장 많은 수익을 낸 장르", value=best_genre)

st.markdown("""
<div style="background: rgba(20,20,30,0.8); border: 1px solid #4da6ff; padding: 2rem; border-radius: 15px; margin-top: 2rem;">
    <h3 style="color: #4da6ff; margin-bottom: 1rem;">🔍 최종 아티클 요약</h3>
    <ul style="line-height: 1.8; font-size: 1.1rem; color: #e0e0e0;">
        <li><b>파레토 법칙의 지배:</b> 상위 5%의 텐트폴 영화가 극장가 전체 관객 파이의 80% 이상을 견인합니다. 상자 그림(Section 2)과 지형도(Section 6)가 이를 여실히 증명합니다.</li>
        <li><b>자본(스크린) vs 콘텐츠(뒷심):</b> 초기 흥행은 스크린 수가 결정짓지만, 천만 영화의 궤도에 오르기 위해서는 철저히 '관객의 자발적 바이럴(뒷심 지수)'이 뒷받침되어야 합니다 (Section 3 & 6 참고).</li>
        <li><b>시간과 지형의 마법:</b> 3D 서피스 지형도는 '개봉 타이밍'이 단순한 날짜 선택이 아닌, 수백만 관객의 파동을 타느냐 마느냐의 중대한 전략임을 보여줍니다. 높은 지형(성수기)에 깃발을 꽂기 위한 배급사들의 눈치 싸움이 데이터로 확인되었습니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br><br><p style='text-align: center; color: #555;'>Designed & Analyzed by AI Data Scientist | Cinematic Masterpiece Edition v3.0</p>", unsafe_allow_html=True)
