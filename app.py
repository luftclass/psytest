import streamlit as st
import time

# --------------------------------------------------------------------------------
# 1. 페이지 및 공통 CSS 설정
# --------------------------------------------------------------------------------
st.set_page_config(page_title="진로 & 학습 통합 진단 시스템", page_icon="🧭", layout="centered")

st.markdown("""
    <style>
    /* 공통 스타일 */
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
    
    /* 메뉴 카드 스타일 */
    .menu-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        background-color: #f8f9fa;
        text-align: center;
        margin-bottom: 10px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .menu-card:hover {
        transform: scale(1.02);
        background-color: #e9ecef;
        border-color: #3498DB;
    }
    
    /* 라디오 버튼 커스텀 */
    .stRadio label {font-size: 18px !important; cursor: pointer;}
    .stRadio > div {gap: 15px;}
    div[role="radiogroup"] > label > div:first-child {display: none;}
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# 2. 세션 상태 초기화 및 관리
# --------------------------------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'main'  # main, test1, test2

# 테스트 상태 초기화 함수
def reset_test_state():
    st.session_state.current_idx = 0
    st.session_state.finished = False
    
    # Test 1 변수 (학습역량)
    st.session_state.lie_score = 0
    st.session_state.main_score = 0
    st.session_state.lie_detected_flag = False
    
    # Test 2 변수 (진로학과 - RIASEC)
    st.session_state.riasec_scores = {'R':0, 'I':0, 'A':0, 'S':0, 'E':0, 'C':0}

if 'current_idx' not in st.session_state:
    reset_test_state()

# 홈으로 가기 함수
def go_home():
    st.session_state.page = 'main'
    reset_test_state()
    st.rerun()

# --------------------------------------------------------------------------------
# 3. 데이터 정의
# --------------------------------------------------------------------------------

# [TEST 1] 학습 역량 진단 문항 (30문항)
questions_test1 = [
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

# [TEST 2] 진로 및 학과 추천 문항 (30문항)
questions_test2 = [
    ("나는 기계를 조립하거나 도구를 사용하여 무언가를 고치는 것을 좋아한다.", "R"),
    ("나는 수학 문제를 풀거나 과학적 원리를 탐구하는 것이 재미있다.", "I"),
    ("나는 글쓰기, 그림 그리기, 음악 연주 등 창의적인 활동을 즐긴다.", "A"),
    ("나는 다른 사람의 고민을 들어주고 도와주는 일에 보람을 느낀다.", "S"),
    ("나는 사람들 앞에서 발표하거나 리더가 되어 이끄는 것을 좋아한다.", "E"),
    ("나는 계획을 세우고 규칙에 따라 체계적으로 일하는 것을 선호한다.", "C"),
    ("나는 야외에서 몸을 움직이며 활동하는 것을 실내 활동보다 좋아한다.", "R"),
    ("나는 새로운 지식을 배우고 복잡한 문제를 논리적으로 분석하는 것을 좋아한다.", "I"),
    ("나는 남들과 다른 독창적인 아이디어를 내는 것을 즐긴다.", "A"),
    ("나는 친구들에게 공부를 가르쳐주거나 봉사활동 하는 것을 좋아한다.", "S"),
    ("나는 사람들을 설득하여 내 의견을 따르게 하는 것에 자신이 있다.", "E"),
    ("나는 숫자나 데이터를 다루고 장부(용돈기입장 등)를 정리하는 것이 편하다.", "C"),
    ("나는 손재주가 있어서 물건을 만들거나 수리하는 데 소질이 있다.", "R"),
    ("나는 현미경 관찰이나 실험을 통해 사실을 검증하는 과정을 좋아한다.", "I"),
    ("나는 영화, 연극, 전시회 등 예술적인 분위기를 좋아하고 감수성이 풍부하다.", "A"),
    ("나는 여러 사람과 어울려 대화하고 친밀한 관계를 맺는 것을 중요하게 생각한다.", "S"),
    ("나는 목표를 달성하기 위해 도전하고 경쟁에서 이기는 것을 즐긴다.", "E"),
    ("나는 정해진 매뉴얼이나 순서에 따라 꼼꼼하게 일 처리하는 것을 잘한다.", "C"),
    ("나는 드론, 로봇, 자동차 등 기계 장치 작동 원리에 관심이 많다.", "R"),
    ("나는 사회 현상이나 자연 현상에 대해 '왜 그럴까?'라고 깊이 생각한다.", "I"),
    ("나는 나만의 개성을 표현할 수 있는 옷차림이나 꾸미기에 관심이 많다.", "A"),
    ("나는 아픈 사람을 돌보거나 사회적 약자를 돕는 일에 관심이 있다.", "S"),
    ("나는 동아리 회장이나 반장처럼 조직을 관리하는 역할을 맡고 싶다.", "E"),
    ("나는 준비물을 챙기거나 서류를 정리하는 등 꼼꼼함이 필요한 일을 잘한다.", "C"),
    ("나는 컴퓨터 하드웨어를 다루거나 기술적인 장비를 다루는 것이 흥미롭다.", "R"),
    ("나는 인공지능, 빅데이터 등 첨단 기술이나 학문에 대한 호기심이 강하다.", "I"),
    ("나는 소설, 시나리오, 웹툰 등 스토리를 창작하는 것을 좋아한다.", "A"),
    ("나는 친구 사이의 갈등을 중재하고 화해시키는 역할을 종종 한다.", "S"),
    ("나는 창업을 하거나 새로운 프로젝트를 기획하여 돈을 버는 것에 관심이 있다.", "E"),
    ("나는 노트 필기를 깔끔하게 하거나 자료를 체계적으로 분류하는 것을 좋아한다.", "C")
]

# 결과 데이터 (RIASEC 유형별 부산/경남 소재 실제 학과 10개씩 추천)
majors_mapping = {
    "R": {
        "title": "🔧 현실형 (Realistic) - 뚝딱뚝딱 엔지니어",
        "desc": "솔직하고 성실하며, 기계나 도구를 다루는 기술적 능력이 뛰어납니다.",
        "majors": [
            "부산대 | 기계공학부",
            "한국해양대 | 기관시스템공학부",
            "창원대 | 스마트제조융합전공",
            "부경대 | 냉동공조공학과",
            "인제대(김해) | 드론IoT시뮬레이션학부",
            "동아대 | 건축학과",
            "경상국립대 | 항공우주및소프트웨어공학부",
            "경남대 | 기계공학부",
            "동의대 | 소방방재행정학과",
            "한국폴리텍(창원) | 스마트전기과"
        ]
    },
    "I": {
        "title": "🔬 탐구형 (Investigative) - 논리적인 탐험가",
        "desc": "지적 호기심이 많고, 논리적이며 과학적인 탐구 활동을 선호합니다.",
        "majors": [
            "부산대 | 화공생명환경공학부",
            "UNIST(울산) | 에너지화학공학과",
            "인제대(김해) | 약학과",
            "경상국립대(진주) | 수의학과",
            "부경대 | 빅데이터융합전공",
            "동아대 | 생명과학과",
            "고신대 | 의예과",
            "부산대 | 물리학과",
            "창원대 | 컴퓨터공학과",
            "인제대(김해) | 임상병리학과"
        ]
    },
    "A": {
        "title": "🎨 예술형 (Artistic) - 창의적인 아티스트",
        "desc": "상상력이 풍부하고 감수성이 예민하며, 자유분방한 창의적 활동을 즐깁니다.",
        "majors": [
            "동서대 | 영상애니메이션학과",
            "부산대 | 시각디자인전공",
            "경성대 | 연극영화학부",
            "동아대 | 산업디자인학과",
            "창원대 | 웹툰전공",
            "부산예술대 | 실용음악과",
            "인제대(김해) | 웹툰영상학과",
            "경남대 | 미디어영상학과",
            "신라대 | 주얼리디자인학과",
            "영산대 | 패션디자인학과"
        ]
    },
    "S": {
        "title": "💛 사회형 (Social) - 따뜻한 멘토",
        "desc": "사람을 좋아하고 이해심이 많으며, 타인을 돕고 가르치는 활동에 보람을 느낍니다.",
        "majors": [
            "부산교대 | 초등교육과",
            "인제대(김해) | 간호학과",
            "부산대 | 특수교육과",
            "신라대 | 상담심리학과",
            "동의대 | 물리치료학과",
            "경남대 | 사회복지학과",
            "가야대(김해) | 특수교육과",
            "동명대 | 언어치료청각학과",
            "영산대 | 항공관광학과",
            "창원대 | 유아교육과"
        ]
    },
    "E": {
        "title": "🔥 진취형 (Enterprising) - 열정적인 리더",
        "desc": "리더십이 있고 외향적이며, 목표를 달성하고 타인을 설득하는 능력이 있습니다.",
        "majors": [
            "부산대 | 경영학과",
            "부경대 | 국제통상학부",
            "동아대 | 관광경영학과",
            "경성대 | 호텔관광외식경영학부",
            "해양대 | 해운경영학부",
            "경남대 | 경찰학부",
            "인제대(김해) | 경영학부",
            "동의대 | 신문방송학과",
            "부산외대 | 마케팅학부",
            "영산대 | 경찰행정학과"
        ]
    },
    "C": {
        "title": "📋 관습형 (Conventional) - 꼼꼼한 매니저",
        "desc": "정확하고 빈틈이 없으며, 체계적인 정리와 데이터 관리에 능숙합니다.",
        "majors": [
            "부경대 | 통계·데이터사이언스전공",
            "부산대 | 문헌정보학과",
            "동아대 | 금융학과",
            "경상국립대 | 회계세무학부",
            "인제대(김해) | 보건행정학과",
            "창원대 | 세무학과",
            "동의대 | 물류시스템공학과",
            "부산외대 | 회계·세무무역학부",
            "동서대 | 정보보호학과",
            "부산가톨릭대 | 병원경영학과"
        ]
    }
}

# --------------------------------------------------------------------------------
# 4. 로직 함수 (Test 1, Test 2 분기 처리)
# --------------------------------------------------------------------------------

def handle_choice():
    idx = st.session_state.current_idx
    selected_val = st.session_state[f"q_{idx}"]
    
    # 1. 학습역량 진단 로직
    if st.session_state.page == 'test1':
        q_type = questions_test1[idx][1]
        if q_type == "lie":
            st.session_state.lie_score += selected_val
            if selected_val == 5:
                st.session_state.lie_detected_flag = True
        else:
            st.session_state.main_score += selected_val
        
        if idx + 1 < len(questions_test1):
            st.session_state.current_idx += 1
        else:
            st.session_state.finished = True
            
    # 2. 진로학과 진단 로직
    elif st.session_state.page == 'test2':
        q_type = questions_test2[idx][1] # R, I, A, S, E, C 중 하나
        st.session_state.riasec_scores[q_type] += selected_val
        
        if idx + 1 < len(questions_test2):
            st.session_state.current_idx += 1
        else:
            st.session_state.finished = True

# --------------------------------------------------------------------------------
# 5. UI 렌더링
# --------------------------------------------------------------------------------

# [화면 1] 메인 메뉴 (Main Menu)
if st.session_state.page == 'main':
    st.markdown('<p class="main-title">🏫 학생 종합 진단 시스템</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">본인에게 필요한 진단을 선택하여 진행해주세요.</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🧠 현재 나의 학습 상태는?")
        if st.button("1. 학습 역량 정밀 진단 (1.1)", use_container_width=True):
            reset_test_state()
            st.session_state.page = 'test1'
            st.rerun()
        st.caption("30문항 | 학습 습관, 메타인지, 동기 분석")

    with col2:
        st.success("🧭 나에게 어울리는 학과는?")
        if st.button("2. 나의 진로와 학과는?", use_container_width=True):
            reset_test_state()
            st.session_state.page = 'test2'
            st.rerun()
        st.caption("30문항 | 홀랜드 적성 검사 기반 학과 추천")

# [화면 2 & 3] 테스트 진행 화면 (공통 UI 사용)
elif st.session_state.page in ['test1', 'test2']:
    
    # ------------------ 결과 화면 ------------------
    if st.session_state.finished:
        st.markdown('<p class="main-title">🎉 진단 결과 분석</p>', unsafe_allow_html=True)
        with st.spinner("결과를 분석하고 있습니다..."):
            time.sleep(0.8)
        
        # [Test 1 결과 처리] 학습 역량
        if st.session_state.page == 'test1':
            score = st.session_state.main_score
            lie_score = st.session_state.lie_score
            lie_flag = st.session_state.lie_detected_flag
            
            if lie_score >= 16 or lie_flag:
                st.error("🚫 신뢰도 낮음: 솔직하지 않은 응답이 감지되었습니다. 재검사가 필요합니다.")
            else:
                st.balloons()
                # 10단계 로직
                level = 1
                if score <= 34: level = 1
                elif score <= 44: level = 2
                elif score <= 54: level = 3
                elif score <= 64: level = 4
                elif score <= 74: level = 5
                elif score <= 84: level = 6
                elif score <= 94: level = 7
                elif score <= 104: level = 8
                elif score <= 114: level = 9
                else: level = 10
                
                titles = {
                    1: "잠재된 씨앗", 2: "깨어나는 새싹", 3: "서툰 걸음마", 4: "호기심 관찰자",
                    5: "기초 건축가", 6: "성실한 러너", 7: "전략적 항해사", 8: "견고한 성주",
                    9: "혁신적 개척자", 10: "통찰의 마스터"
                }
                
                st.success(f"당신의 학습 레벨: Level {level}. {titles[level]} (점수: {score}/125)")
                st.info("💡 자세한 분석 내용은 선생님께 상담을 요청하거나 상세 리포트를 확인하세요.")
                
                # 추가 상세 내용을 원하시면 이전 코드의 상세 분석 텍스트를 이곳에 복원하면 됩니다.
        
        # [Test 2 결과 처리] 진로 학과 (수정된 부분)
        elif st.session_state.page == 'test2':
            st.balloons()
            scores = st.session_state.riasec_scores
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top_type = sorted_scores[0][0]
            second_type = sorted_scores[1][0]
            
            result_data = majors_mapping[top_type]
            
            st.markdown(f"### 🏆 당신의 핵심 유형: **{result_data['title']}**")
            st.info(f"💡 **유형 특징:** {result_data['desc']}")
            
            st.divider()
            
            st.markdown(f"### 🏫 부산/경남권 추천 학과 (Top 10)")
            st.markdown(f"학생의 **'{top_type}'** 성향에 적합한 우리 지역(부산/경남/김해) 실제 학과입니다.")
            
            # 카드 형태로 깔끔하게 출력
            for major in result_data['majors']:
                univ, dept = major.split("|")
                st.markdown(f"""
                <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 8px; background-color: #f9f9f9;">
                    <span style="font-weight:bold; color: #2C3E50;">{univ.strip()}</span> 
                    <span style="float:right; color: #3498DB; font-weight:bold;">{dept.strip()}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
            st.caption(f"※ 2순위 추천 유형: {majors_mapping[second_type]['title']}")

        st.markdown("---")
        if st.button("🏠 메인 화면으로 돌아가기"):
            go_home()

    # ------------------ 질문 진행 화면 ------------------
    else:
        idx = st.session_state.current_idx
        
        # 질문 가져오기
        if st.session_state.page == 'test1':
            q_text, _ = questions_test1[idx]
            total_q = len(questions_test1)
            title_text = "학습 역량 정밀 진단"
        else:
            q_text, _ = questions_test2[idx]
            total_q = len(questions_test2)
            title_text = "나의 진로와 학과는?"
        
        st.markdown(f"### {title_text}")
        st.progress((idx / total_q), text=f"진행률 ({idx + 1}/{total_q})")
        
        st.markdown(f"""
            <div class="question-box">
                Q{idx+1}. {q_text}
            </div>
        """, unsafe_allow_html=True)
        
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
            on_change=handle_choice
        )
        
        # 테스트 중 중단하고 나가기 버튼
        st.markdown("---")
        if st.button("🔙 홈으로 나가기 (진행 내용 초기화)"):
            go_home()
