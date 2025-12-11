import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(page_title="동물로 보는 본능 테스트", page_icon="🐾", layout="centered")

# 2. CSS 스타일링 (다크모드 지원 + 카드 디자인)
st.markdown("""
    <style>
    /* 전체 폰트 및 배경 설정 */
    .main-title {
        font-size: 32px; 
        font-weight: bold; 
        text-align: center; 
        margin-bottom: 10px; 
        color: #4A4A4A;
    }
    .sub-title {
        font-size: 18px; 
        text-align: center; 
        color: #888; 
        margin-bottom: 30px;
    }
    
    /* 질문 박스 스타일 */
    .question-box {
        padding: 30px; 
        border-radius: 20px; 
        margin-bottom: 25px;
        background-color: #ffffff; 
        border: 3px solid #E0F7FA;
        color: #333333 !important; /* 다크모드에서도 검은 글씨 강제 */
        font-size: 20px;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* 결과 카드 스타일 */
    .result-card {
        padding: 30px;
        border-radius: 20px;
        background-color: #f9f9f9;
        border: 2px solid #eee;
        text-align: center;
        color: #333333 !important;
        margin-bottom: 20px;
    }
    .animal-name {
        font-size: 28px; 
        font-weight: bold; 
        color: #2c3e50; 
        margin: 15px 0;
    }
    .animal-emoji {
        font-size: 80px;
    }
    
    /* 라디오 버튼 폰트 키우기 */
    div[role="radiogroup"] > label > div:first-child {
        display: none;
    }
    .stRadio label {
        font-size: 18px !important;
        padding: 10px;
        border-radius: 10px;
        transition: background-color 0.3s;
    }
    .stRadio label:hover {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화 (변수 저장용)
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'lie_score' not in st.session_state:
    st.session_state.lie_score = 0
if 'main_score' not in st.session_state:
    st.session_state.main_score = 0
if 'finished' not in st.session_state:
    st.session_state.finished = False

# 4. 질문 데이터 (총 15문항: 타당성 3 + 본질문 12)
questions = [
    ("사소한 마찰이 생겼을 때, 굳이 상황을 키우기보다 조용히 넘어가는 편이 더 효율적이라고 느낀다.", "main"),
    ("나는 살면서 단 한 번도, 상황을 모면하기 위해 사소한 거짓말이나 핑계를 대본 적이 없다.", "lie"),
    ("경제적으로 부담이 될 때는 약속이나 의무도 재조정이 필요하다고 생각한다.", "main"),
    ("단체에 문제가 생겼을 때, 조직 전체를 위해 개인이 책임을 떠안는 것도 현실적인 선택일 수 있다.", "main"),
    ("나는 살면서 마음속으로조차 타인을 흉보거나 미워한 적이 단 한 번도 없다.", "lie"),
    ("경쟁 상황에서는 정보를 활용하여 우위를 점하는 능력도 하나의 실력이라고 생각한다.", "main"),
    ("가까운 사람의 슬픔을 이해는 하지만, 감정에 오래 머무르는 것은 생산적이지 않다고 느낀다.", "main"),
    ("아무도 보지 않고 피해도 없다면, 굳이 엄격한 규칙 준수에 얽매일 필요는 없다고 본다.", "main"),
    ("문제가 커지지 않도록 상황 설명을 조금 조정하는 것은 사회생활의 필요한 기술이다.", "main"),
    ("결과가 좋다면 과정상의 작은 원칙들은 어느 정도 유연하게 해석될 수 있다고 생각한다.", "main"),
    ("나는 무례하거나 부당한 대우를 받아도, 화가 나거나 짜증이 난 적이 전혀 없다.", "lie"),
    ("사회적 피해를 입은 사람에게도, 상황을 피하지 못한 개인의 판단 책임이 일정 부분 있다고 본다.", "main"),
    ("갈등 상황에서는 진실한 감정을 나누기보다, 상황을 원만하게 빨리 정리하는 것이 더 중요하다.", "main"),
    ("부탁을 잘 거절하지 못하는 사람에게 일을 요청하는 것도 일종의 자원 활용 능력이다.", "main"),
    ("제도의 빈틈을 찾아내어 활용하는 것은 불법이 아니라 능력의 한 형태다.", "main")
]

# 5. 헤더 화면 출력
st.markdown('<p class="main-title">🐾 숨겨진 본능 찾기 테스트</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">당신의 사회생활 스타일을 동물에 비유한다면?</p>', unsafe_allow_html=True)
st.markdown("---")

# --------------------------------------------------------------------------------
# A. 결과 화면 (5가지 동물 유형 + 히든 유형)
# --------------------------------------------------------------------------------
if st.session_state.finished:
    lie_score = st.session_state.lie_score
    main_score = st.session_state.main_score
    
    # 0. 신뢰도 검증 실패 (히든 유형: 카멜레온)
    if lie_score >= 11:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="animal-emoji">🦎</div>', unsafe_allow_html=True)
        st.markdown('<p class="animal-name">"속을 알 수 없는 가면 쓴 카멜레온"</p>', unsafe_allow_html=True)
        st.error(f"⚠️ 타당도 경고: {lie_score}점 (너무 완벽하게 보이려 함)")
        st.markdown("""
        **"보호색이 너무 짙으시네요!"**
        
        당신은 본심을 철저히 숨기고 완벽한 모습만 보여주려 하고 있습니다.
        인간이라면 누구나 느끼는 감정조차 부정하셨군요.
        너무 완벽한 연기는 오히려 의심을 사는 법입니다.
        
        **👉 솔직한 모습으로 다시 테스트하면 진짜 본능을 알려드릴게요.**
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # 1. 결과 분석 성공
    else:
        # Level 1: 순수 이타주의 (~21점)
        if main_score <= 21:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="animal-emoji">🐶</div>', unsafe_allow_html=True)
            st.markdown('<p class="animal-name">"눈물 많은 골든 리트리버"</p>', unsafe_allow_html=True)
            st.success(f"본능 지수: {main_score}점 (순수 공감형)")
            st.markdown("""
            **"세상 모든 게 다 내 친구!"**
            * **특징:** 의심 없고 사람을 너무 좋아합니다. 자신의 이익보다 남의 기분을 먼저 살피는 '평화지킴이'입니다.
            * **강점:** 당신 주변엔 항상 사람이 끊이지 않습니다. 최고의 친화력을 가졌습니다.
            * **주의:** 나쁜 의도를 가진 사람에게 '호구' 잡히기 딱 좋습니다. 거절하는 법을 배우세요!
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        # Level 2: 평화주의 (~31점)
        elif main_score <= 31:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="animal-emoji">🦫</div>', unsafe_allow_html=True)
            st.markdown('<p class="animal-name">"상처받지 않는 무던한 카피바라"</p>', unsafe_allow_html=True)
            st.info(f"본능 지수: {main_score}점 (평화 유지형)")
            st.markdown("""
            **"좋은 게 좋은 거지~ (목욕 중)"**
            * **특징:** 웬만해선 화를 내지 않고 물 흐르듯 살아갑니다. 갈등 상황을 극도로 싫어해 조용히 넘어가는 편입니다.
            * **강점:** 어떤 조직에 가도 모난 돌이 되지 않고 잘 적응합니다. 멘탈 관리를 잘합니다.
            * **주의:** 우유부단해 보일 수 있습니다. 정말 중요한 문제에서는 확실한 목소리를 내야 합니다.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        # Level 3: 현실적 균형 (~41점)
        elif main_score <= 41:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="animal-emoji">🐬</div>', unsafe_allow_html=True)
            st.markdown('<p class="animal-name">"사회생활 만렙 눈치 빠른 돌고래"</p>', unsafe_allow_html=True)
            st.info(f"본능 지수: {main_score}점 (현실 적응형)")
            st.markdown("""
            **"IQ 점프! 낄끼빠빠의 귀재"**
            * **특징:** 도덕과 실리 사이에서 줄타기를 아주 잘합니다. 적당히 착하고, 적당히 이기적인 가장 현실적인 타입입니다.
            * **강점:** 상황 파악이 빠르고 처세술이 좋습니다. 어디서 굶어 죽을 일은 없는 똑똑한 사람입니다.
            * **주의:** 너무 머리를 굴리다 보면 진심을 의심받을 수 있습니다. 가끔은 계산 없는 모습을 보여주세요.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        # Level 4: 전략적 실리 (~51점)
        elif main_score <= 51:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="animal-emoji">🦊</div>', unsafe_allow_html=True)
            st.markdown('<p class="animal-name">"실속 챙기는 매력적인 붉은 여우"</p>', unsafe_allow_html=True)
            st.warning(f"본능 지수: {main_score}점 (전략가형)")
            st.markdown("""
            **"내 몫은 내가 챙겨야지?"**
            * **특징:** 원하는 것을 얻기 위해 자신의 매력과 정보를 이용할 줄 압니다. 감정보다는 이득을 먼저 계산합니다.
            * **강점:** 효율성의 화신입니다. 남들이 감정에 빠져 허우적댈 때, 당신은 이미 목표를 달성하고 퇴근합니다.
            * **주의:** '여우 같다'는 뒷말이 나올 수 있습니다. 신뢰를 잃지 않도록 선을 지키는 것이 중요합니다.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        # Level 5: 냉철한 승부사 (52점~)
        else:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="animal-emoji">🦅</div>', unsafe_allow_html=True)
            st.markdown('<p class="animal-name">"자비 없는 하늘의 제왕 검독수리"</p>', unsafe_allow_html=True)
            st.error(f"본능 지수: {main_score}점 (지배자형)")
            st.markdown("""
            **"감정은 사냥에 방해될 뿐이다."**
            * **특징:** 목표를 위해서라면 수단과 방법을 가리지 않는 냉혹한 승부사입니다. 타인을 도구로 보는 경향이 강합니다.
            * **강점:** 위기 상황에서 흔들리지 않는 멘탈과 압도적인 성과 창출 능력을 가졌습니다. 리더의 자질이 있습니다.
            * **주의:** 높은 곳은 춥고 외롭습니다. 성공 끝에 고립되지 않으려면 주변을 돌아보는 연습이 필요합니다.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    # 재시작 버튼
    if st.button("🐾 다른 동물로 다시 태어나기", type="primary"):
        st.session_state.current_idx = 0
        st.session_state.lie_score = 0
        st.session_state.main_score = 0
        st.session_state.finished = False
        st.rerun()

# --------------------------------------------------------------------------------
# B. 질문 진행 화면 (수정됨: 자동 넘기기 적용)
# --------------------------------------------------------------------------------
else:
    # 진행률 표시
    idx = st.session_state.current_idx
    q_text, q_type = questions[idx]
    
    progress = int((idx / len(questions)) * 100)
    st.progress(progress, text=f"본능 탐색 중... {progress}%")
    
    # 질문 박스
    st.markdown(f"""
        <div class="question-box">
            {q_text}
        </div>
    """, unsafe_allow_html=True)

    # ---[핵심 변경 사항] 콜백 함수 정의---
    def handle_click():
        """라디오 버튼 선택 시 실행되는 함수"""
        # 현재 질문의 키값(q_{idx})으로 선택된 값을 가져옴
        current_val = st.session_state[f"q_{idx}"]
        
        # 점수 합산
        if q_type == "lie":
            st.session_state.lie_score += current_val
        else:
            st.session_state.main_score += current_val
            
        # 다음 인덱스로 이동하거나 종료 처리
        if st.session_state.current_idx + 1 < len(questions):
            st.session_state.current_idx += 1
        else:
            st.session_state.finished = True

    # 답변 선택 (라디오 버튼)
    # on_change=handle_click 을 추가하여 선택 즉시 함수가 실행되게 함
    st.radio(
        "솔직하게 선택해주세요 👇",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "전혀 아니다 (1점)",
            2: "아니다 (2점)",
            3: "보통이다 (3점)",
            4: "그렇다 (4점)",
            5: "매우 그렇다 (5점)"
        }[x],
        index=None,         # 초기 선택 없음
        key=f"q_{idx}",     # 고유 키
        on_change=handle_click  # 선택 시 자동 실행
    )
    
    # 더 이상 '다음' 버튼이 필요 없음
