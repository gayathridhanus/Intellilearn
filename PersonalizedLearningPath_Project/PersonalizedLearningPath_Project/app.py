import streamlit as st
import pandas as pd
import plotly.express as px
from config import COURSES, QUESTION_BANK
from database import init_db, create_student, get_students, save_attempt, get_history
from knowledge_tracing import estimate_mastery
from recommendation import recommend_topics

st.set_page_config(page_title="IntelliLearn", page_icon="🎓", layout="wide")
init_db()
st.title("IntelliLearn")
st.caption("Knowledge tracing • Adaptive practice • Learning analytics")

with st.sidebar:
    st.header("Learner")
    name = st.text_input("Student name", placeholder="Enter your name")
    if st.button("Create / Select Student", use_container_width=True):
        try:
            st.session_state.student = create_student(name)
            st.success("Student selected")
        except ValueError as exc:
            st.error(str(exc))
    students = get_students()
    if students:
        selected = st.selectbox("Existing learner", students, format_func=lambda x: x["name"])
        if st.button("Use selected learner", use_container_width=True):
            st.session_state.student = selected
    st.divider()
    page = st.radio("Navigation", ["Dashboard", "Take a Quiz", "About Project"])

student = st.session_state.get("student")
if not student:
    st.info("Create or select a learner in the sidebar to begin.")
    st.write("Choose a course, attempt a quiz, and then view your personalized learning path.")
    st.stop()

if page == "Take a Quiz":
    st.subheader("Quiz Practice")
    course = st.selectbox("Course", list(COURSES))
    concepts = [x["name"] for x in COURSES[course]]
    concept = st.selectbox("Concept", concepts)
    questions = QUESTION_BANK.get(concept, [])
    with st.form("quiz"):
        responses = []
        for i, (question, options, answer) in enumerate(questions):
            choice = st.radio(f"Q{i+1}. {question}", options, key=f"{course}-{concept}-{i}")
            responses.append((question, options.index(choice), answer))
        submit = st.form_submit_button("Submit quiz", type="primary")
    if submit:
        score = 0
        for question, chosen, answer in responses:
            correct = int(chosen == answer)
            score += correct
            save_attempt(student["id"], course, concept, question, correct)
        st.success(f"Your score: {score}/{len(responses)} ({score/len(responses):.0%}). Results saved.")

elif page == "Dashboard":
    st.subheader(f"Learning Dashboard — {student['name']}")
    course = st.selectbox("Course", list(COURSES))
    cfg = COURSES[course]
    concepts = [x["name"] for x in cfg]
    history = get_history(student["id"], course)
    mastery, is_dkt = estimate_mastery(history, concepts)
    a, b, c = st.columns(3)
    a.metric("Quiz questions attempted", len(history))
    b.metric("Correct answers", int(history["is_correct"].sum()) if len(history) else 0)
    c.metric("Average accuracy", f"{history['is_correct'].mean():.0%}" if len(history) else "—")
    st.caption("Mastery estimate: trained TensorFlow DKT model" if is_dkt else
               "Mastery estimate: smoothed quiz-history baseline. Train the DKT model to enable model predictions.")
    chart = pd.DataFrame({"Concept": concepts, "Estimated mastery": [mastery[x] for x in concepts]})
    st.plotly_chart(px.bar(chart, x="Concept", y="Estimated mastery", range_y=[0,1],
                           title="Concept Mastery", text_auto=".0%"), use_container_width=True)
    st.subheader("Recommended Learning Path")
    recs = recommend_topics(cfg, mastery)
    if recs:
        for i, r in enumerate(recs, 1):
            st.markdown(f"**{i}. {r['concept']}** — {r['difficulty']} — mastery {r['mastery']:.0%}")
            st.caption(r["reason"])
    else:
        st.success("Good progress! No topic currently needs priority practice.")
    st.subheader("Quiz History")
    if history.empty:
        st.info("No attempts yet. Take a quiz to populate this section.")
    else:
        st.dataframe(history.tail(20).iloc[::-1], use_container_width=True, hide_index=True)
        st.download_button("Export history (CSV)", history.to_csv(index=False).encode("utf-8"),
                           "learning_history.csv", "text/csv")

else:
    st.subheader("About IntelliLearn")

    st.write("""
    IntelliLearn is an intelligent adaptive learning application
    designed to understand students' learning abilities and provide
    personalized topic recommendations based on their quiz performance.
    """)

    st.markdown("""
    ### Key Features

    - **Learner Management:** Manage student profiles.
    - **Course Management:** Explore courses and learning concepts.
    - **Quiz Assessment:** Evaluate knowledge through interactive quizzes.
    - **Knowledge Tracing:** Estimate concept mastery using TensorFlow/Keras.
    - **Smart Recommendations:** Suggest topics that need more practice.
    - **Learning Analytics:** Visualize student progress and export reports.

    ### Technologies Used

    - Python
    - TensorFlow / Keras
    - Streamlit
    - SQLite
    - Pandas and NumPy
    - Plotly

    ### How IntelliLearn Works

    1. Register or select a student.
    2. Choose a course and attempt quizzes.
    3. The system records quiz performance.
    4. The knowledge tracing model estimates concept mastery.
    5. The recommendation engine suggests topics for improvement.
    6. Track your learning progress through the dashboard.

    ### Research Note

    The current demonstration model uses synthetic training sequences.
    Its predictions should not be interpreted as validated real-student
    learning outcomes. Real educational datasets and held-out testing
    are required for research evaluation.
    """)

    st.divider()

    st.markdown(
        "<div style='text-align:center; color:gray;'>"
        "🎓 IntelliLearn | Learn Smarter. Grow Faster."
        "</div>",
        unsafe_allow_html=True
    )
