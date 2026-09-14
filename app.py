import streamlit as st
import random
import pandas as pd
from pathlib import Path


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="숫자 맞히기 게임",
    page_icon="🎯",
    layout="centered"
)


# =========================================================
# 파일 설정
# =========================================================

LEADERBOARD_FILE = Path("leaderboard.csv")


# =========================================================
# CSS 디자인
# =========================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(
            135deg,
            #eef2ff 0%,
            #f8fafc 50%,
            #ecfeff 100%
        );
    }

    /* 제목 */
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #4f46e5;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* 게임 박스 */
    .game-card {
        background: white;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin-bottom: 25px;
    }

    /* 성공 박스 */
    .success-card {
        background: linear-gradient(
            135deg,
            #dcfce7,
            #ecfdf5
        );
        border: 2px solid #22c55e;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .success-title {
        color: #15803d;
        font-size: 32px;
        font-weight: 800;
    }

    .success-text {
        color: #166534;
        font-size: 20px;
    }

    /* 랭킹 */
    .ranking-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #1e293b;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    /* 버튼 */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        min-height: 45px;
        font-weight: 700;
    }

    /* 숫자 입력 */
    input {
        border-radius: 10px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 랭킹 파일 생성
# =========================================================

def create_leaderboard_file():

    if not LEADERBOARD_FILE.exists():

        df = pd.DataFrame(
            columns=[
                "name",
                "attempts"
            ]
        )

        df.to_csv(
            LEADERBOARD_FILE,
            index=False
        )


# =========================================================
# 랭킹 불러오기
# =========================================================

def load_leaderboard():

    create_leaderboard_file()

    try:

        df = pd.read_csv(
            LEADERBOARD_FILE
        )

        if df.empty:
            return pd.DataFrame(
                columns=[
                    "name",
                    "attempts"
                ]
            )

        # 시도 횟수를 숫자로 변환
        df["attempts"] = pd.to_numeric(
            df["attempts"],
            errors="coerce"
        )

        # 잘못된 데이터 제거
        df = df.dropna(
            subset=["attempts"]
        )

        df["attempts"] = df[
            "attempts"
        ].astype(int)

        # 적은 시도 횟수가 먼저
        df = df.sort_values(
            by="attempts",
            ascending=True
        ).reset_index(
            drop=True
        )

        return df

    except Exception:

        return pd.DataFrame(
            columns=[
                "name",
                "attempts"
            ]
        )


# =========================================================
# 점수 저장
# =========================================================

def save_score(name, attempts):

    df = load_leaderboard()

    new_score = pd.DataFrame(
        [
            {
                "name": name,
                "attempts": attempts
            }
        ]
    )

    df = pd.concat(
        [
            df,
            new_score
        ],
        ignore_index=True
    )

    # 시도 횟수 순으로 정렬
    df = df.sort_values(
        by="attempts",
        ascending=True
    ).reset_index(
        drop=True
    )

    # 최대 100명
    df = df.head(100)

    df.to_csv(
        LEADERBOARD_FILE,
        index=False
    )


# =========================================================
# 새 게임 시작
# =========================================================

def start_new_game():

    # 1~100 중 랜덤 숫자
    st.session_state.target_number = random.randint(
        1,
        100
    )

    # 시도 횟수
    st.session_state.attempts = 0

    # 게임 종료 여부
    st.session_state.game_over = False

    # 힌트
    st.session_state.hint = ""

    # 마지막 입력 숫자
    st.session_state.last_guess = None

    # 랭킹 저장 여부
    st.session_state.score_saved = False


# =========================================================
# 세션 상태 초기화
# =========================================================

if "target_number" not in st.session_state:

    start_new_game()


# =========================================================
# 제목
# =========================================================

st.markdown(
    '<div class="title">🎯 숫자 맞히기 게임</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '컴퓨터가 생각한 1부터 100 사이의 숫자를 맞혀보세요!'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 게임 카드 시작
# =========================================================

st.markdown(
    '<div class="game-card">',
    unsafe_allow_html=True
)

st.subheader("🔢 숫자를 입력하세요")

# 숫자 입력
guess = st.number_input(
    "1부터 100까지의 숫자",
    min_value=1,
    max_value=100,
    value=50,
    step=1,
    disabled=st.session_state.game_over
)


# =========================================================
# 맞히기 버튼
# =========================================================

if not st.session_state.game_over:

    if st.button(
        "🎯 숫자 맞히기",
        type="primary"
    ):

        # 시도 횟수 증가
        st.session_state.attempts += 1

        # 입력 숫자 저장
        st.session_state.last_guess = guess

        # 정답
        target = st.session_state.target_number

        # UP
        if guess < target:

            st.session_state.hint = (
                "🔼 UP! 더 큰 숫자입니다."
            )

        # DOWN
        elif guess > target:

            st.session_state.hint = (
                "🔽 DOWN! 더 작은 숫자입니다."
            )

        # 정답
        else:

            st.session_state.hint = (
                f"🎉 정답입니다! "
                f"정답은 {target}입니다."
            )

            st.session_state.game_over = True


# =========================================================
# 힌트 표시
# =========================================================

if st.session_state.hint:

    if st.session_state.game_over:

        st.markdown(
            f"""
            <div class="success-card">

                <div class="success-title">
                    🎉 정답입니다!
                </div>

                <div class="success-text">
                    {st.session_state.hint}
                </div>

                <br>

                <div class="success-text">
                    총 시도 횟수:
                    <strong>
                        {st.session_state.attempts}회
                    </strong>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            st.session_state.hint
        )


# =========================================================
# 게임 정보
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        label="🎯 현재 시도",
        value=f"{st.session_state.attempts}회"
    )


with col2:

    if st.session_state.game_over:

        st.metric(
            label="🎉 정답",
            value=st.session_state.target_number
        )

    else:

        st.metric(
            label="🔢 숫자 범위",
            value="1 ~ 100"
        )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 랭킹 등록
# =========================================================

if st.session_state.game_over:

    st.divider()

    st.subheader("🏆 랭킹 등록")

    if not st.session_state.score_saved:

        player_name = st.text_input(
            "닉네임을 입력하세요",
            max_chars=20,
            placeholder="예: 홍길동"
        )

        if st.button(
            "🏆 랭킹에 기록하기",
            type="primary"
        ):

            player_name = player_name.strip()

            if not player_name:

                st.warning(
                    "닉네임을 입력해주세요."
                )

            else:

                save_score(
                    player_name,
                    st.session_state.attempts
                )

                st.session_state.score_saved = True

                st.success(
                    "🎉 랭킹에 성공적으로 등록되었습니다!"
                )

                st.rerun()

    else:

        st.success(
            "✅ 이미 랭킹에 기록되었습니다."
        )


# =========================================================
# 새 게임 버튼
# =========================================================

st.divider()

if st.button(
    "🔄 새 게임 시작"
):

    start_new_game()

    st.rerun()


# =========================================================
# 랭킹 표시
# =========================================================

st.markdown(
    '<div class="ranking-title">'
    '🏆 명예의 전당'
    '</div>',
    unsafe_allow_html=True
)


leaderboard = load_leaderboard()


if leaderboard.empty:

    st.info(
        "아직 등록된 기록이 없습니다.\n\n"
        "첫 번째 기록의 주인공이 되어보세요! 🎯"
    )

else:

    # 상위 10명
    top10 = leaderboard.head(10).copy()

    # 순위 생성
    top10.insert(
        0,
        "순위",
        range(
            1,
            len(top10) + 1
        )
    )

    # 표시 이름 변경
    top10.columns = [
        "순위",
        "닉네임",
        "시도 횟수"
    ]

    # 1~3위 강조
    for index, row in top10.iterrows():

        rank = row["순위"]

        if rank == 1:

            st.success(
                f"🥇 1위  |  "
                f"**{row['닉네임']}**  |  "
                f"{row['시도 횟수']}회"
            )

        elif rank == 2:

            st.info(
                f"🥈 2위  |  "
                f"**{row['닉네임']}**  |  "
                f"{row['시도 횟수']}회"
            )

        elif rank == 3:

            st.warning(
                f"🥉 3위  |  "
                f"**{row['닉네임']}**  |  "
                f"{row['시도 횟수']}회"
            )


    # 4위부터 표로 표시
    if len(top10) > 3:

        st.dataframe(
            top10.iloc[3:],
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 게임 방법
# =========================================================

st.divider()

with st.expander("📖 게임 방법"):

    st.markdown(
        """
        ### 🎯 게임 방법

        **1.** 컴퓨터가 1부터 100 사이의 숫자를 하나 선택합니다.

        **2.** 숫자를 입력하고
        `숫자 맞히기` 버튼을 누릅니다.

        **3.** 입력한 숫자가 정답보다 작으면
        `UP`이라는 힌트가 나옵니다.

        **4.** 입력한 숫자가 정답보다 크면
        `DOWN`이라는 힌트가 나옵니다.

        **5.** 정답을 맞히면 게임이 종료됩니다.

        **6.** 닉네임을 입력하면 랭킹에 등록됩니다.

        ### 🏆 랭킹 규칙

        **시도 횟수가 적을수록 높은 순위입니다.**

        예:

        - 4회 → 1위
        - 5회 → 2위
        - 7회 → 3위
        """
    )


# =========================================================
# 하단
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        margin-top:40px;
        margin-bottom:20px;
    ">
        🎯 Number Guessing Game<br>
        Made with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
