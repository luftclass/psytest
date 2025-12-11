import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(page_title="학습 역량 정밀 진단 (30문항)", page_icon="🎓", layout="centered")

# 2. CSS 스타일링
st.markdown("""
    <style>
    .main-title {font-size: 32px; font-weight: bold; text-align: center; margin-bottom: 10px; color: #2C3E50;}
    .sub-title {font-size: 18px; text-align: center; color: #7F8C8D; margin-bottom: 30px;}
    .question-box {
        padding: 30px; 
        border-radius: 15px; 
        margin-bottom: 25px;
        background-color: #ffffff; 
        border: 2px solid #3498DB;
        color: #333333 !important;
        font-size: 20px;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .result-card {
        padding: 25px;
        border-radius: 15px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
        color: #333333 !important;
    }
    /* 라디오 버튼 스타일 */
    .stRadio label {font-size: 18px !important; cursor: pointer;}
    .stRadio > div {gap: 15px;}
    div[role="radiogroup"] > label > div:first-child {display: none;}
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'lie_score' not in st.session_state:
    st.session_state.lie_score = 0
if 'main_score' not in st.session_state:
    st.session_state.main_score = 0
if 'finished' not in st.session_state:
    st.session_state.finished = False
if 'lie_detected_flag' not in st.session_state:
    st.session_state.lie_detected_flag = False

# 4. 질문 데이터 (총 30문항)
questions = [
    ("나는 공부를 시작하기 전에 오늘 무엇을 얼마나 할지 구체적인 계획을 세운다.", "main"),
    ("나는 태어나서 단 한 번도 공부하기 싫다는 생각을 해본 적이 없다.", "lie"),
    ("나는 내가 무엇을 알고 무엇을 모르는지 스스로 명확하게 파악하고 있다.", "main"),
    ("지능이나 재능은 타고나는 것이 아니라 노력하면 얼마든지 발달시킬 수 있다고 믿는다.", "main"),
    ("배운 내용을 무작정 외우기보다 나만의 언어로 요약하거나 구조화해서 이해하려고 한다.", "main"),
    ("수업 시간에 단 1초도 딴생각을 하지 않고 완벽하게 집중한다.", "lie"),
    ("공부 중에 스마트폰이나 게임의 유혹이 생겨도 스스로 통제하고 다시 집중할 수 있다.", "main"),
    ("공부가 잘 안 되거나 모르는 것이 생기면 선생님이나 친구에게 적극적으로 도움을 요청한다.", "main"),
    ("시험 결과가 좋지 않아도 실망하기보다 부족한 점을 찾아 보완하는 기회로 삼는다.", "main"),
    ("나는 계획한 일정을 단 한 번도 어기지 않고 1분 단위까지 완벽하게 지킨다.", "lie"),
    ("좋은 성적을 받는 것보다 새로운 지식을 배우고 성장하는 것 자체에 즐거움을 느낀다.", "main"),
    ("공부에 방해되는 요소(소음, 책상 정리 등)를 스스로 정리하고 집중할 수 있는 환경을 만든다.", "main"),
    ("교과서나 선생님의 설명을 그대로 받아들이기보다 '왜 그럴까?'라고 생각하며 비판적으로 탐구한다.", "main"),
    ("나는 살면서 모르는 문제가 나와도 전혀 답답해하거나 짜증 낸 적이 없다.", "lie"),
    ("새로 배운 내용을 이미 알고 있는 지식이나 경험과 연결하여 이해하려고 노력한다.", "main"),
    ("시험 기간이 아니더라도 평소에 플래너 등을 활용해 시간을 효율적으로 관리한다.", "main"),
    ("나는 노력한다면 아무리 어려운 과제라도 결국 해낼 수 있다는 자신감이 있다.", "main"),
    ("나는 타인에게 인정받고 싶은 마음이나 경쟁심을 단 한 번도 느껴본 적이 없다.", "lie"),
    ("공부한 내용은 잊어버리지 않도록 주기적으로 다시 보며 복습하는 습관이 있다.", "main"),
    ("나의 장래 희망이나 꿈을 이루기 위해 지금의 공부가 필요하다는 것을 명확히 알고 있다.", "main"),
    ("공부를 마친 후 오늘 계획한 것을 얼마나 달성했는지 스스로 평가하고 반성한다.", "main"),
    ("어려운 문제가 풀리지 않아도 포기하지 않고 끝까지 답을 찾으려고 노력한다.", "main"),
    ("공부할 때는 잡념을 버리고 지금 하고 있는 과제에만 몰입하는 편이다.", "main"),
    ("해야 할 일이 많을 때 중요하고 급한 순서대로 우선순위를 정해서 처리한다.", "main"),
    ("누가 시키지 않아도 스스로 필요한 공부를 찾아서 하는 편이다.", "main"),
    ("시험이나 과제 때문에 불안감이 밀려올 때, 긍정적인 생각이나 심호흡으로 스스로 마음을 다잡는다.", "main"),
    ("선생님이나 친구의 비판적인 피드백을 감정적으로 받아들이기보다 성장의 밑거름으로 삼는다.", "main"),
    ("학습한 자료나 프린트물을 나중에 찾기 쉽도록 체계적으로 분류하고 정리한다.", "main"),
    ("배운 내용을 친구들에게 설명해주거나 가르쳐주는 활동을 통해 더 깊이 이해하려고 한다.", "main"),
    ("컨디션이 좋지 않거나 하기 싫은 날에도 최소한의 정해진 분량은 꾸준히 해낸다.", "main")
]

# --------------------------------------------------------------------------------
# 콜백 함수 (선택 즉시 다음 문제로 넘어가는 로직)
# --------------------------------------------------------------------------------
def go_next():
    idx = st.session_state.current_idx
    selected_val = st.session_state[f"q_{idx}"]
    
    q_type = questions[idx][1]
    
    if q_type == "lie":
        st.session_state.lie_score += selected_val
        if selected_val == 5:
            st.session_state.lie_detected_flag = True
    else:
        st.session_state.main_score += selected_val
    
    if idx + 1 < len(questions):
        st.session_state.current_idx += 1
    else:
        st.session_state.finished = True

# --------------------------------------------------------------------------------
# 메인 화면 구성
# --------------------------------------------------------------------------------

# 헤더 영역
st.markdown('<p class="main-title">🎓 학습 역량 정밀 진단 (30문항)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">교육학, 심리학, 뇌과학 이론에 기반한 심층 분석 리포트</p>', unsafe_allow_html=True)
st.markdown("---")

# --------------------------------------------------------------------------------
# 결과 화면
# --------------------------------------------------------------------------------
if st.session_state.finished:
    with st.spinner("결과 분석 중입니다..."):
        time.sleep(0.5)

    lie_score = st.session_state.lie_score
    main_score = st.session_state.main_score
    lie_detected = st.session_state.lie_detected_flag
    
    # 1. 신뢰도 검증 실패
    if lie_score >= 16 or lie_detected:
        st.error(f"🚫 **진단 불가 (신뢰도 저하)**")
        
        st.markdown("""
        **[분석 오류: 사회적 바람직성 편향 (Social Desirability Bias)]**
        
        응답 데이터에서 본인의 실제 모습보다 이상적이거나 완벽한 학습자로 포장하려는 방어 기제가 감지되었습니다.
        
        **⚠️ 구체적인 원인 분석:**
        인간의 뇌는 새로운 지식을 습득하거나 어려운 과제에 직면할 때 필연적으로 **'인지적 갈등(Cognitive Conflict)'**과 **'정서적 저항'**을 경험합니다.
        
        그러나 귀하의 응답은 **"태어나서 한 번도 공부가 싫은 적이 없다"**와 같이 학습 과정에서 발생하는 자연스러운 갈등과 스트레스를 **전면 부정**하고 있습니다. 이는 메타인지(Metacognition)가 작동하지 않고 있음을 시사합니다.
        
        정확한 진단을 위해 본인의 취약한 점까지 솔직하게 인정하는 태도로 **재검사를 권장합니다.**
        """)
        
    # 2. 결과 분석 성공
    else:
        st.balloons()
        
        # Level 1: 0 ~ 50점
        if main_score <= 50:
            st.warning("🌱 **가능성을 품은 새싹 (Beginning Learner)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **자기조절학습(Self-Regulated Learning) 미성숙:** 학습 목표 설정-실행-평가의 순환 고리가 아직 형성되지 않았습니다.
                * **학습된 무기력(Learned Helplessness) 위험:** 반복된 시행착오로 인해 효능감이 낮아져 있어, 작은 실패에도 쉽게 포기할 수 있습니다.
                * **정서적 취약성:** 학습 불안이나 스트레스 상황에서 편도체(Amygdala)가 과활성화되어 인지 기능을 마비시킬 수 있습니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **백지 상태의 가소성(Plasticity):** 고착된 나쁜 습관이 적어, 올바른 개입(Intervention) 시 뇌 신경망의 빠른 재구조화가 가능합니다.
                * **수용적 태도:** 새로운 학습 도구와 방식에 대한 저항감이 낮아 지도를 잘 따를 가능성이 높습니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **비계 설정(Scaffolding):** 혼자 감당하기 힘든 과제는 쪼개서 수행하거나 멘토의 도움을 받아 **근접발달영역(ZPD)**을 점진적으로 확장해야 합니다.
                * **행동 조형(Shaping):** '책상 정리하기' 같은 아주 쉬운 행동부터 시작하여 학습 습관을 단계적으로 형성하세요.
                * **환경 설계:** 의지력에 의존하기보다 스마트폰을 시야에서 치우는 등 물리적 환경을 통제(Nudge)하는 것이 효과적입니다.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **도파민 보상 회로:** '오늘 단어 5개 암기'와 같이 100% 달성 가능한 목표를 세우고 성공 경험을 축적하세요. 작은 성취감이 뇌의 보상 중추를 자극하여 학습 동기를 만듭니다.
                """)

        # Level 2: 51 ~ 75점
        elif main_score <= 75:
            st.info("🔭 **성장하는 탐험가 (Developing Explorer)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **유창성의 착각(Fluency Illusion):** 강의를 '보는 것'을 '아는 것'으로 착각하는 메타인지적 오류가 발생합니다.
                * **외재적 동기 우세:** 스스로의 호기심보다는 성적이나 보상 등 외부 요인에 의해 학습이 좌우됩니다.
                * **정보 처리의 비효율:** 정보를 조직화하지 않고 단순 나열식으로 기억하려 하여 인지 부하(Cognitive Load)가 높습니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **학습 의욕:** 학습의 필요성을 인지하고 있으며, 적절한 동기 부여 시 **수행 목표(Performance Goal)**를 달성하려는 에너지가 충분합니다.
                * **기초 스키마(Schema):** 학습을 위한 기본적인 인지 구조와 배경 지식이 형성되고 있는 단계입니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **인출 연습(Retrieval Practice):** 책을 덮고 배운 내용을 백지에 써보는 인출 과정을 통해 기억 흔적을 강화해야 합니다.
                * **동료 교수(Peer Teaching):** 친구에게 가르쳐주는 활동은 메타인지를 높이는 최고의 전략입니다.
                * **분산 학습:** 벼락치기는 단기 기억에 불과합니다. 시간 간격을 두고 반복하는 분산 학습이 장기 기억 형성에 필수적입니다.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **해마와 수면:** 학습 후 충분한 수면(7시간 이상)은 해마가 단기 기억을 대뇌 피질의 장기 기억으로 전송(Consolidation)하는 필수 시간입니다.
                """)

        # Level 3: 76 ~ 100점
        elif main_score <= 100:
            st.success("🧗 **성실한 등반가 (Diligent Climber)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **우수한 실행 기능(Executive Function):** 충동을 억제하고 주의를 유지하는 전두엽 기능이 탁월합니다.
                * **만족 지연(Delay of Gratification):** 미래의 보상을 위해 현재의 유혹을 참는 그릿(Grit)을 보유했습니다.
                * **전략적 유연성 부족:** 성실함은 뛰어나나, 과제 난이도에 따라 전략을 유연하게 바꾸는 요령이 다소 부족할 수 있습니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **회복 탄력성(Resilience):** 실패를 성장의 발판으로 삼으려는 긍정적 태도가 형성되어 있습니다.
                * **자기 통제력:** 학습 환경과 정서를 스스로 모니터링하고 통제하는 능력이 뛰어납니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **정교화 시연(Elaborative Rehearsal):** 새로운 지식을 기존 지식과 연결하고 '왜?'라고 질문하며 깊이 있게 파고드세요.
                * **이중 부호화(Dual Coding):** 텍스트와 시각 자료(도표, 마인드맵)를 동시에 활용하여 정보 처리 효율을 극대화하세요.
                * **전이(Transfer) 훈련:** 배운 원리를 다른 맥락에 적용해보는 연습을 통해 응용력을 길러야 합니다.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **전두엽 에너지 관리:** 50분 집중 후 10분 휴식 시 스마트폰을 멀리하고 멍하니 있거나(DMN 활성화) 가벼운 산책을 하여 인지 자원을 재충전하세요.
                """)

        # Level 4: 101 ~ 125점
        else:
            st.success("👑 **통찰력 있는 마스터 (Master Learner)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **자기결정성(Self-Determination) 실현:** 내재적 동기에 의해 학습을 주도하며 자율성, 유능성 욕구가 충족되었습니다.
                * **숙달 목표 지향(Mastery Goal):** 경쟁보다 배움 그 자체와 자기 성장을 최우선 가치로 둡니다.
                * **메타인지의 자동화:** 학습 조절 과정이 무의식적이고 자연스럽게 이루어지는 경지에 도달했습니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **비판적/창의적 사고:** 정보를 분석, 평가, 재구성하여 새로운 가치를 창출합니다.
                * **정서 지능(Emotional Intelligence):** 학습 스트레스를 도전으로 받아들이며 긍정적으로 조절합니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **교차 학습(Interleaved Practice):** 서로 다른 유형의 문제를 섞어서 풀며 문제 해결의 유연성을 극대화하세요.
                * **메타인지적 발문:** "이것이 최선의 방법인가?", "이 지식의 한계는 무엇인가?" 등 본질적인 질문을 던지세요.
                * **지식의 구조화:** 단편적 지식을 연결하여 거대한 지식의 네트워크(빅픽처)를 구축하세요.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **시냅스 연결과 통찰:** 서로 관련 없어 보이는 지식을 연결(Connect)하여 창의적 통찰(Insight)이 폭발하는 **'아하 모먼트'**를 자주 경험해 보세요.
                """)

    # 재시작 버튼
    if st.button("🔄 테스트 다시 하기", type="primary"):
        st.session_state.current_idx = 0
        st.session_state.lie_score = 0
        st.session_state.main_score = 0
        st.session_state.finished = False
        st.session_state.lie_detected_flag = False
        st.rerun()

# --------------------------------------------------------------------------------
# 질문 진행 화면
# --------------------------------------------------------------------------------
else:
    idx = st.session_state.current_idx
    q_text, q_type = questions[idx]
    
    # 진행률
    progress = int((idx / len(questions)) * 100)
    st.progress(progress, text=f"역량 진단 중... ({idx + 1}/{len(questions)})")
    
    # 질문 박스
    st.markdown(f"""
        <div class="question-box">
            {q_text}
        </div>
    """, unsafe_allow_html=True)
    
    # 답변 선택 (클릭 즉시 다음 문제로 이동)
    st.radio(
        "자신에게 해당하는 정도를 선택하세요:",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "전혀 아니다 (1점)",
            2: "아니다 (2점)",
            3: "보통이다 (3점)",
            4: "그렇다 (4점)",
            5: "매우 그렇다 (5점)"
        }[x],
        index=None,
        key=f"q_{idx}",
        on_change=go_next
    )
