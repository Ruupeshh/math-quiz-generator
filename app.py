import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt
from quiz_logic import generate_question
from storage import save_result, load_history

# Sidebar title
st.sidebar.title("Math Quiz Generator")
# nav menu on the side
page = st.sidebar.radio("Menu", ["Take Quiz", "Score History"])

# Take Quiz Page
if page == "Take Quiz":
    st.title("Ready to Boost Your Math Skills?")
    st.markdown("Choose your quiz settings on the left and press **Start Quiz** to begin!")
    st.markdown("---")

    # settings sidebar
    with st.sidebar.expander("Quiz Settings", expanded=True):
        operations = {"Mixed": 'mixed', "Plus (+)": "+", "Minus (-)": "-", "Times (×)": "×", "Divide (÷)": "÷"}
        operations_label = st.selectbox("Pick operation", list(operations.keys()))
        operation = operations[operations_label]  # actual symbol

        difficulty_labels = ["Easy", "Medium", "Hard"]
        difficulty = st.selectbox("Pick difficulty", difficulty_labels)

        no_question = st.slider("How many questions?", 1, 20, 5)

    # init when quiz starts
    if "quiz_started" not in st.session_state:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.quiz_started = False
        st.session_state.start_time = None

    # button to start quiz
    if st.button("Start Quiz"):
        st.session_state.quiz_started = True
        st.session_state.questions = [generate_question(operation, difficulty) for i in range(no_question)]
        st.session_state.answers = [""] * no_question
        st.session_state.start_time = datetime.now()

    # if quiz started, show questions
    if st.session_state.quiz_started:
        st.subheader("Questions Time!")

        # ask each question
        for i, (first, second, op, correct) in enumerate(st.session_state.questions):
            ans = st.text_input(f"{i+1}. {first} {op} {second}", key=f"ans_{i}")
            st.session_state.answers[i] = ans

        # submit answers and show result
        if st.button("Submit Answers"):
            st.subheader("Results")
            score = 0

            for i, (first, second, op, correct) in enumerate(st.session_state.questions):
                inp = st.session_state.answers[i]
                try:
                    val = int(inp)
                    if val == correct:
                        st.write(f"{first} {op} {second} = {val} ✔️")
                        score += 1
                    else:
                        st.write(f"{first} {op} {second} = {val} x (should be {correct})")
                except:
                    st.write(f"{first} {op} {second} = {inp} invalid input!")

            # calculate time and accuracy
            time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
            accuracy = str(round(score / no_question * 100, 2))
            st.write(f"Your score: {score}/{no_question}")
            st.write(f"Your accuracy: {accuracy}%")
            st.write(f"Time taken: {round(time_taken, 2)} seconds")

            # save to file (json)
            save_result(score, no_question, accuracy, op, difficulty, time_taken)

            # reset so quiz can start fresh again
            st.session_state.quiz_started = False


# Score History Page
elif page == "Score History":
    st.title("Score History & Insights")
    history = load_history()

    if history:
        df = pd.DataFrame(history)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["accuracy"] = df["accuracy"].astype(float)

        # score over time chart
        st.write("### Accuracy Over Time")
        chart = alt.Chart(df).mark_line(point=True).encode(
            x='timestamp:T',
            y='accuracy:Q',
            color='operation:N',
            tooltip=['timestamp', 'score', 'total', 'accuracy', 'operation', 'difficulty', 'time_taken']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

        # time vs accuracy chart
        st.write("### Time Taken vs Accuracy")
        chart2 = alt.Chart(df).mark_circle(size=100).encode(
            x='time_taken:Q',
            y='accuracy:Q',
            color='difficulty:N',
            tooltip=['timestamp', 'score', 'total', 'accuracy', 'time_taken', 'difficulty']
        ).interactive()
        st.altair_chart(chart2, use_container_width=True)

        # bar chart for difficulty
        st.write("### Average Accuracy by Difficulty")
        avg_acc = df.groupby('difficulty')["accuracy"].mean().reset_index()
        chart3 = alt.Chart(avg_acc).mark_bar().encode(
            x='difficulty:N',
            y='accuracy:Q'
        )
        st.altair_chart(chart3, use_container_width=True)

        # table of past attempts
        st.write("### Recent Attempts")
        st.dataframe(df.sort_values("timestamp", ascending=False).head(5))
    else:
        st.info("No history yet. Try taking a quiz!")
