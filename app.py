import streamlit as st

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
    .stRadio label {font-size: 18px !important;}
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

# 4. 질문 데이터 (총 30문항: 타당도 5 + 학습역량 25)
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
    # --- 추가된 5문항 ---
    ("시험이나 과제 때문에 불안감이 밀려올 때, 긍정적인 생각이나 심호흡으로 스스로 마음을 다잡는다.", "main"),
    ("선생님이나 친구의 비판적인 피드백을 감정적으로 받아들이기보다 성장의 밑거름으로 삼는다.", "main"),
    ("학습한 자료나 프린트물을 나중에 찾기 쉽도록 체계적으로 분류하고 정리한다.", "main"),
    ("배운 내용을 친구들에게 설명해주거나 가르쳐주는 활동을 통해 더 깊이 이해하려고 한다.", "main"),
    ("컨디션이 좋지 않거나 하기 싫은 날에도 최소한의 정해진 분량은 꾸준히 해낸다.", "main")
]

# 헤더 영역
st.markdown('<p class="main-title">🎓 학습 역량 정밀 진단 (30문항)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">교육학, 심리학, 뇌과학 이론에 기반한 심층 분석 리포트</p>', unsafe_allow_html=True)
st.markdown("---")

# --------------------------------------------------------------------------------
# 결과 화면
# --------------------------------------------------------------------------------
if st.session_state.finished:
    lie_score = st.session_state.lie_score
    main_score = st.session_state.main_score
    lie_detected = st.session_state.lie_detected_flag
    
    # 1. 신뢰도 검증 실패 (기준: 16점 이상 OR 결정적 거짓말 탐지)
    if lie_score >= 16 or lie_detected:
        st.error(f"🚫 **진단 불가 (신뢰도 저하)**")
        reason = "결정적 모순 응답(Lie Scale 5점)" if lie_detected else f"타당도 총점 초과 ({lie_score}/25점)"
        st.write(f"**원인:** {reason}")
        
        st.markdown("""
        **[분석 오류: 사회적 바람직성 편향 (Social Desirability Bias)]**
        
        응답 데이터에서 본인의 모습을 지나치게 이상적인 학습자로 포장하려는 방어 기제가 감지되었습니다.
        예를 들어, "태어나서 한 번도 공부가 싫은 적이 없다"와 같은 문항에 긍정하는 것은 인지적 갈등을 전면 부정하는 것으로, 이는 실제 학습 태도와 괴리가 큽니다.
        
        이 상태에서는 메타인지와 학습 습관을 정확히 분석할 수 없습니다. **솔직한 태도로 재검사를 권장합니다.**
        """)
        
    # 2. 결과 분석 (본문항 25개 * 5점 = 125점 만점)
    else:
        st.balloons()
        
        # Level 1: 0 ~ 50점
        if main_score <= 50:
            st.warning("🌱 **가능성을 품은 새싹 (Beginning Learner)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **자기조절학습(Self-Regulated Learning)의 미성숙:** 학습 목표를 설정하고, 실행 전략을 수립하며, 결과를 평가하는 일련의 메타인지적 순환 고리가 아직 형성되지 않았습니다. 학습을 '해야 한다'는 당위성은 인지하지만, 실행 동력이 부족합니다.
                * **학습된 무기력(Learned Helplessness)의 위험:** 반복된 시행착오나 실패 경험으로 인해 "노력해도 결과는 바뀌지 않을 것"이라는 부정적 신념이 기저에 자리 잡고 있어, 학업적 자기효능감(Self-Efficacy)이 저하된 상태입니다.
                * **정서적 취약성 및 회피 동기:** 학습 상황에서 발생하는 불안이나 스트레스에 취약하며, 과제를 해결하기보다는 미루거나 회피하려는 방어적 태도가 관찰됩니다. 편도체의 과활성화로 인해 전두엽의 이성적 판단이 방해받기 쉽습니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **백지 상태의 신경 가소성(Neuroplasticity):** 잘못 고착된 학습 습관이나 편견(Bad Habits)이 적어, 올바른 교육적 개입(Intervention)이 이루어질 경우 뇌 신경망이 빠르고 효율적으로 재구조화될 수 있는 최적의 상태입니다.
                * **수용적 태도와 유연성:** 자신의 고집을 내세우기보다 새로운 학습 도구, 멘토의 조언, 변화된 학습 방식을 거부감 없이 받아들일 준비가 되어 있어, 지도 효과가 높게 나타날 가능성이 큽니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **비계 설정(Scaffolding)을 통한 근접발달영역(ZPD) 확장:** 혼자서는 해결하기 벅찬 과제를 억지로 붙들고 있기보다, 교사나 멘토의 도움을 받아 과제를 세분화하여 수행함으로써 '성공 경험'을 축적해야 합니다.
                * **행동 조형(Shaping) 기법 적용:** '1시간 공부하기' 같은 거창한 목표 대신, '책상 정리하기', '교과서 펴기'와 같이 저항감이 없는 아주 작은 행동부터 시작하여 학습 행동을 점진적으로 강화해야 합니다.
                * **환경 설계를 통한 넛지(Nudge):** 의지력은 고갈되는 자원입니다. 공부할 때 스마트폰을 시야에서 완전히 치우거나, 학습 전용 공간을 분리하는 등 물리적 환경 통제를 통해 주의력 분산을 원천 차단해야 합니다.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **도파민(Dopamine) 보상 회로의 재설계:** 거대한 목표 달성 시에만 보상을 주지 마세요. '오늘 단어 5개 암기'와 같이 100% 달성 가능한 마이크로 목표를 세우고, 이를 달성할 때마다 뇌의 측좌핵(Nucleus Accumbens)을 자극하여 학습 동기의 선순환 구조를 만들어야 합니다.
                """)

        # Level 2: 51 ~ 75점
        elif main_score <= 75:
            st.info("🔭 **성장하는 탐험가 (Developing Explorer)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **유창성의 착각(Fluency Illusion):** 강의를 '보는 것(Passive Learning)'을 자신이 '아는 것(Active Knowledge)'으로 착각하는 메타인지적 오류가 빈번합니다. 이해했다고 느끼지만 막상 설명하려 하면 막히는 현상이 나타납니다.
                * **외재적 조절(External Regulation) 우세:** 지적 호기심이나 배움의 즐거움보다는 성적, 부모님의 칭찬, 입시 등 외부 보상이나 처벌 회피에 의해 학습 행동이 좌우되는 경향이 강합니다.
                * **정보 처리의 비효율성:** 지식을 유의미하게 조직화(Organization)하거나 구조화하지 않고, 단순 나열식으로 암기하려 하여 인지 부하(Cognitive Load)가 높고 망각 속도가 빠릅니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **수행 목표(Performance Goal)에 기반한 에너지:** 학습의 필요성을 인지하고 있으며, 경쟁 상황이나 시험 기간 등 명확한 목표가 주어졌을 때 이를 달성하고자 하는 강력한 에너지를 발휘할 수 있습니다.
                * **기초 스키마(Schema)의 형성:** 학습을 위한 기본적인 인지 구조와 배경 지식이 형성되고 있는 단계로, 적절한 전략만 더해진다면 폭발적인 성장이 가능한 '임계점'에 도달해 있습니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **인출 연습(Retrieval Practice)의 생활화:** 단순히 텍스트를 재독(Re-reading)하는 것은 비효율적입니다. 책을 덮고 배운 내용을 백지에 인출해 보는 과정을 통해 장기 기억 흔적을 강화해야 합니다.
                * **동료 교수(Peer Teaching) 활용:** 친구에게 가르쳐주는 활동은 메타인지를 높이는 최고의 전략입니다. 남에게 설명할 수 없다면 그것은 온전한 내 지식이 아님을 인지해야 합니다.
                * **분산 학습(Distributed Practice):** 벼락치기(집중 학습)는 단기 기억에 머물다 사라집니다. 학습 간격을 두고 반복하는 분산 학습이 시냅스 연결을 강화하여 기억의 영속성을 보장합니다.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **해마(Hippocampus)와 기억 응고화(Consolidation):** 학습 후 충분한 수면(7시간 이상)은 해마가 낮 동안의 단기 기억을 대뇌 피질의 장기 기억으로 전송하고 저장하는 필수적인 시간입니다. 밤샘 공부는 뇌의 저장 기능을 끄고 정보를 쏟아붓는 것과 같습니다.
                """)

        # Level 3: 76 ~ 100점
        elif main_score <= 100:
            st.success("🧗 **성실한 등반가 (Diligent Climber)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **우수한 실행 기능(Executive Function):** 전두엽의 인지 통제 기능이 잘 발달하여, 즉각적인 충동을 억제하고 장기적인 목표를 위해 주의를 지속적으로 유지하는 능력이 탁월합니다.
                * **만족 지연(Delay of Gratification) 능력:** 미래의 더 큰 보상을 위해 현재의 즐거움이나 유혹을 유보할 줄 아는 높은 수준의 그릿(Grit)과 자제력을 보유하고 있습니다.
                * **전략적 유연성의 한계:** 성실함과 끈기는 최고 수준이나, 과목의 특성이나 과제의 난이도에 따라 학습 전략을 유연하게 수정(Adaptation)하는 요령이 다소 부족하여 '열심히 하지만 비효율적인' 구간에 갇힐 수 있습니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **높은 회복 탄력성(Resilience):** 시험을 망치거나 실패를 겪어도 좌절에 머무르지 않고, 이를 피드백으로 삼아 빠르게 회복하고 더 높은 단계로 도약하려는 긍정적 태도가 형성되어 있습니다.
                * **자기 통제 및 관리 능력:** 물리적 학습 환경뿐만 아니라 자신의 정서 상태까지 스스로 모니터링하고 통제하는 능력이 뛰어나, 슬럼프 관리에 능합니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **정교화 시연(Elaborative Rehearsal):** 새로운 지식을 기존의 지식과 연결하고, '왜 그럴까?'라고 끊임없이 질문하며 의미를 확장하는 심층 처리(Deep Processing) 학습이 필요합니다.
                * **이중 부호화(Dual Coding) 이론 적용:** 텍스트 정보뿐만 아니라 도표, 그래프, 마인드맵 등 시각적 정보를 동시에 활용하여 뇌의 정보 처리 채널을 다각화하고 효율을 극대화하세요.
                * **전이(Transfer) 훈련:** 배운 원리를 교과서 밖의 전혀 다른 문제 상황이나 실생활에 적용해보는 연습을 통해, 죽은 지식이 아닌 살아있는 응용력을 길러야 합니다.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **전두엽의 에너지 관리와 휴식:** 높은 자기 통제는 뇌의 에너지원인 포도당을 급격히 소모시킵니다. 50분 집중 후에는 스마트폰을 보지 않고 멍하니 있거나(DMN 활성화) 가벼운 산책을 하여 고갈된 인지 자원을 주기적으로 재충전해야 번아웃을 막을 수 있습니다.
                """)

        # Level 4: 101 ~ 125점
        else:
            st.success("👑 **통찰력 있는 마스터 (Master Learner)**")
            st.caption(f"학습 역량 지수: {main_score} / 125")
            
            with st.expander("📊 교육심리학적 심층 분석 보고서", expanded=True):
                st.markdown("""
                **1. 🔍 정밀 진단 (Diagnosis)**
                * **자기결정성(Self-Determination)의 완전한 실현:** 자율성, 유능성, 관계성의 기본 심리 욕구가 충족된 상태로, 외부의 강요가 아닌 순수한 내재적 동기에 의해 학습을 주도합니다.
                * **숙달 목표 지향(Mastery Goal Orientation):** 타인과의 경쟁에서 이기는 것(수행 목표)보다, 배움 그 자체의 즐거움과 어제보다 성장하는 것(숙달 목표)을 최우선 가치로 둡니다.
                * **메타인지의 자동화(Automatization):** 학습 계획 수립, 모니터링, 전략 수정, 결과 평가의 일련의 과정이 의식적인 노력 없이도 무의식적이고 자연스럽게 이루어지는 경지에 도달했습니다.

                **2. ✨ 잠재 강점 (Strengths)**
                * **고차원적 비판적 사고(Critical Thinking):** 지식을 수동적으로 수용하는 단계를 넘어, 정보를 분석하고 평가하며 재구성하여 자신만의 관점을 정립하는 능력이 탁월합니다.
                * **높은 정서 지능(Emotional Intelligence):** 학습 과정에서 오는 불안이나 스트레스를 위협이 아닌 도전으로 받아들이며, 부정적 감정을 스스로 긍정적으로 승화시키는 정서 조절 능력을 갖추었습니다.

                **3. 💡 전문 솔루션 (Solution)**
                * **교차 학습(Interleaved Practice):** 한 가지 유형만 집중적으로 파는 블록 학습보다, 서로 다른 유형의 문제나 과목을 교차하며 학습하여 뇌의 변별력과 문제 해결의 유연성을 극대화하세요.
                * **메타인지적 발문(Self-Questioning):** "이것이 최선의 해결책인가?", "이 지식의 반례나 한계는 무엇인가?" 등 끊임없이 본질적인 질문을 던지며 사고의 깊이를 더하고 지식의 경계를 확장하세요.
                * **지식의 구조화와 빅픽처:** 단편적인 지식들을 연결하여 거대한 지식의 네트워크를 구축하고, 학문 간의 경계를 넘나드는 융합적 사고를 지향하세요.

                **4. 🧠 뇌과학적 조언 (Neuroscience)**
                * **시냅스 가지치기와 가소성의 정점:** 당신의 뇌는 이미 비효율적인 경로를 제거하고 최적화된 신경망 고속도로를 구축했습니다. 이제는 서로 관련 없어 보이는 이질적인 지식들을 연결(Connect)하여, 창의적 통찰(Insight)이 폭발하는 **'아하 모먼트(Aha Moment)'**를 의도적으로 만들어내야 할 때입니다.
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
    
    # 답변 선택
    choice = st.radio(
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
        key=f"q_{idx}"
    )
    
    # 다음 버튼
    if st.button("다음 문항 >", type="primary", use_container_width=True):
        if choice is None:
            st.warning("⚠️ 답변을 선택해주세요!")
        else:
            if q_type == "lie":
                st.session_state.lie_score += choice
                if choice == 5:
                    st.session_state.lie_detected_flag = True
            else:
                st.session_state.main_score += choice
            
            if idx + 1 < len(questions):
                st.session_state.current_idx += 1
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()
