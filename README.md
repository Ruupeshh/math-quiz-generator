# Math Quiz Generator

This is my final project for **Computer Programming II**. It’s a math quiz app built using **Streamlit**.

The user can choose what kind of math problems they want (like addition, subtraction, multiplication, division, or mixed), and also the difficulty level (Easy, Medium, Hard). Then the app generates random questions and the user has to answer them. At the end, it shows your score, accuracy, and how long you took.

The app also saves your results to a JSON file so you can view your past attempts and see how you're doing over time. There's a separate page where you can see charts (like your scores and accuracy over time).

## How to Run

Make sure you have Python installed. Then:

```bash
pip install streamlit pandas altair
streamlit run app.py
```

---

## Files Included

* `app.py`: Main Streamlit app
* `quiz_logic.py`: Contains the logic to generate math questions
* `storage.py`: Code to save/load quiz results
* `data/score_history.json`: Stores your past quiz results
* `README.md`: (this file)
* `demo.mp4`: demo of the app working

---

## Author

* Name: *\Rupesh Shrestha*
* Course: Computer Programming II – Section 002
* Date: May 5 2025

## Sources Referenced

* https://docs.streamlit.io/
* https://github.com/streamlit/docs
* https://www.datacamp.com/tutorial/streamlit
* https://altair-viz.github.io/
