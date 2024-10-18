import streamlit as st
import random

# List of categories and their respective items (10 words per category)
categories = {
    "لاعبي كرة القدم": ["ميسي", "رونالدو", "مبابي", "نيمار", "صلاح", "ليفاندوفسكي", "بنزيمة", "كين", "هالاند", "مودريتش"],
    "الحيوانات": ["كلب", "قط", "فيل", "أسد", "نمر", "حصان", "زرافة", "كنغر", "باندا", "دلفين"],
    "الملابس": ["قميص", "بنطلون", "قبعة", "سترة", "جوارب", "وشاح", "بلوفر", "أحذية", "حزام", "قفازات"],
    "الفواكه": ["تفاح", "موز", "برتقال", "فراولة", "عنب", "مانجو", "أناناس", "كرز", "خوخ", "بطيخ"]
}

# Initialize session state to store the game state
if 'step' not in st.session_state:
    st.session_state.step = 'setup'
    st.session_state.players = []
    st.session_state.imposter = None
    st.session_state.detective = None
    st.session_state.silencer = None
    st.session_state.current_player_index = 0
    st.session_state.category = None
    st.session_state.word_for_in_players = None
    st.session_state.asked_players = []
    st.session_state.answered_players = []
    st.session_state.word_choices = []
    st.session_state.scores = {}  # To track scores of players and imposter
    st.session_state.show_guide = True  # Flag for showing guide
    st.session_state.event_active = False  # To track if the event is enabled
    st.session_state.double_points_this_round = False  # Track if double points is active for the current round
    st.session_state.game_mode = None  # Track if we are in classic or advanced mode

# Sidebar for setup
with st.sidebar:
    st.title("إعداد اللعبة")

    # Select game mode (Classic or Advanced)
    st.session_state.game_mode = st.selectbox("اختر وضع اللعبة", ["كلاسيكي", "متقدم"])

    # Select category
    st.session_state.category = st.selectbox("اختر الفئة", list(categories.keys()))

    # Get number of players
    num_players = st.number_input('أدخل عدد اللاعبين', min_value=3, max_value=10, step=1)

    # Collect players' names
    players = []
    for i in range(num_players):
        player_name = st.text_input(f'أدخل اسم اللاعب {i+1}', key=f'player_{i}')
        if player_name:
            players.append(player_name)

    # Event Activation Checkbox
    st.session_state.event_active = st.checkbox("تفعيل الحدث؟ (احتمال 20% لمضاعفة النقاط)")

    # Button to start the game
    if st.button('ابدأ اللعبة') and len(players) == num_players:
        st.session_state.players = players
        st.session_state.imposter = random.choice(players)
        st.session_state.word_for_in_players = random.choice(categories[st.session_state.category])

        if st.session_state.game_mode == "متقدم":
            # Assign a Detective and a Silencer randomly (different from imposter)
            roles_players = [p for p in players if p != st.session_state.imposter]
            st.session_state.detective = random.choice(roles_players)
            roles_players.remove(st.session_state.detective)
            st.session_state.silencer = random.choice(roles_players)

        # Initialize scores
        for player in players:
            st.session_state.scores[player] = 0
        st.session_state.scores[st.session_state.imposter] = 0  # Imposter's score initialization

        st.session_state.step = 'reveal'
        st.session_state.current_player_index = 0
        st.session_state.show_guide = False  # Hide the guide

# Main content area
st.title("برا القصة - Out of the Story")

# Game Guide
if st.session_state.show_guide:
    with st.expander("Game Guide", expanded=True):
        st.write("""
        Welcome to the game! Here’s how to play:

        1. **Setup**: Enter the number of players (minimum 3) and their names. Choose a category for the words.
        2. **Reveal**: Each player will take turns to reveal if they are "IN" or "OUT" of the story. The imposter will be selected randomly.
        3. **Questioning Phase**: Players will ask questions to each other to find out who the imposter is. 
        4. **Guessing Phase**: After questioning, players will guess who they think the imposter is.
        5. **Imposter Guessing**: The imposter will then guess the word that the other players know from a set of choices.
        6. **Scoring**: Players earn points for correctly guessing the imposter, and the imposter earns points for guessing the correct word.

        If the **Event** is active, there will be a 20% chance to double points for this round!

        In **Advanced Mode**, two additional roles are introduced:
        - **Detective**: Tries to uncover the imposter.
        - **Silencer**: Must avoid revealing their identity while assisting the imposter.

        Have fun and may the best player win!

        Game By Haider
        """)

if st.session_state.step == 'reveal':
    player = st.session_state.players[st.session_state.current_player_index]

    st.write(f"أعط الهاتف إلى {player} لمعرفة ما إذا كان داخل أو خارج القصة.")

    if st.button(f"{player}, اضغط لعرض النتيجة"):
        if player == st.session_state.imposter:
            st.error(f"{player}, أنت خارج القصة!")
        else:
            st.success(f"{player}, أنت داخل القصة! الكلمة الخاصة بك هي: {st.session_state.word_for_in_players}")

        if st.session_state.game_mode == "متقدم":
            if player == st.session_state.detective:
                st.info(f"{player}, أنت **المحقق**!")
            elif player == st.session_state.silencer:
                st.warning(f"{player}, أنت **الصامت**!")

        if st.session_state.current_player_index < len(st.session_state.players) - 1:
            st.session_state.current_player_index += 1
        else:
            # Event Trigger: 20% chance for double points if the event is active
            if st.session_state.event_active:
                st.session_state.double_points_this_round = random.random() < 0.2
                if st.session_state.double_points_this_round:
                    st.warning("تم تفعيل حدث مضاعفة النقاط! سيتم مضاعفة النقاط هذه الجولة!")
                else:
                    st.info("لا يوجد حدث هذه الجولة.")
            else:
                st.session_state.double_points_this_round = False

            st.session_state.step = 'Questioning'
            st.session_state.current_player_index = 0

if st.session_state.step == 'Questioning':
    st.write("مرحلة الأسئلة: حاول العثور على المحتال!")

    current_asker = st.session_state.players[st.session_state.current_player_index]

    available_answerers = [p for p in st.session_state.players if p != current_asker and p not in st.session_state.answered_players]
    if not available_answerers:
        available_answerers = [p for p in st.session_state.players if p != current_asker]

    selected_answerer = random.choice(available_answerers)

    st.write(f"{current_asker} يسأل {selected_answerer}. اسأل سؤالك بصوت عالٍ!")

    st.session_state.asked_players.append(current_asker)
    st.session_state.answered_players.append(selected_answerer)

    if st.button("السؤال التالي"):
        if st.session_state.current_player_index < len(st.session_state.players) - 1:
            st.session_state.current_player_index += 1
        else:
            if len(set(st.session_state.asked_players)) < len(st.session_state.players):
                st.session_state.current_player_index = 0
            else:
                st.session_state.step = 'guess_imposter'
                st.session_state.current_player_index = 0

if st.session_state.step == 'guess_imposter':
    st.write("حان الوقت لتخمين المحتال!")

    guesses = []
    for player in st.session_state.players:
        guess = st.selectbox(f"{player}, من تعتقد أنه المحتال؟", st.session_state.players, key=f'guess_{player}')
        guesses.append((player, guess))

    if st.button('إرسال التخمينات'):
        for player, guess in guesses:
            if guess == st.session_state.imposter:
                points = 100
                if st.session_state.double_points_this_round:
                    points *= 2  # Double the points if the event triggers
                st.session_state.scores[player] += points

        st.write(f"المحتال هو: {st.session_state.imposter}!")
        st.session_state.step = 'imposter_guess'

if st.session_state.step == 'imposter_guess':
    st.write(f"{st.session_state.imposter}, الآن دورك لتخمين الكلمة!")

    if not st.session_state.word_choices:
        st.session_state.word_choices = random.sample(categories[st.session_state.category], 4)

    imposter_guess = st.selectbox(f"{st.session_state.imposter}, ما هي الكلمة التي يعتقد الآخرون أنها في القصة؟", st.session_state.word_choices)

    if st.button('إرسال تخمين المحتال'):
        if imposter_guess == st.session_state.word_for_in_players:
            points = 200
            if st.session_state.double_points_this_round:
                points *= 2  # Double the points if the event triggers
            st.session_state.scores[st.session_state.imposter] += points

        st.session_state.step = 'results'

if st.session_state.step == 'results':
    st.write("النتائج النهائية!")
    for player, score in st.session_state.scores.items():
        st.write(f"{player}: {score} نقاط")

    if st.button("ابدأ جولة جديدة"):
        st.session_state.step = 'setup'
        st.session_state.current_player_index = 0
        st.session_state.asked_players = []
        st.session_state.answered_players = []
        st.session_state.word_choices = []
        st.session_state.show_guide = True
