from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "quizsecret"

questions = [
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "define", "def", "func"],
        "answer": "def"
    },
    {
        "question": "Which data type is used to store text in Python?",
        "options": ["int", "str", "float", "bool"],
        "answer": "str"
    },
    {
        "question": "Who created Python?",
        "options": ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"],
        "answer": "Guido van Rossum"
    },
    {
        "question": "Which loop is used to iterate over a sequence in Python?",
        "options": ["for", "while", "loop", "repeat"],
        "answer": "for"
    },
    {
        "question": "Which of the following is used to take input from the user in Python?",
        "options": ["input()", "scan()", "read()", "get()"],
        "answer": "input()"
    }
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz", methods=["GET","POST"])
def quiz():

    if "current_question" not in session:
        session["current_question"] = 0
        session["answers"] = []

    if request.method == "POST":

        action = request.form.get("action")
        answer = request.form.get("answer")

        q_index = session["current_question"]

        # Save answer
        if len(session["answers"]) > q_index:
            session["answers"][q_index] = answer
        else:
            session["answers"].append(answer)

        # NEXT button
        if action == "next":
            session["current_question"] += 1

        # PREVIOUS button
        elif action == "prev":
            session["current_question"] -= 1

    q_index = session["current_question"]

    if q_index >= len(questions):
        return redirect(url_for("result"))

    if q_index < 0:
        session["current_question"] = 0
        q_index = 0

    question = questions[q_index]

    return render_template(
        "quiz.html",
        question=question,
        q_index=q_index,
        total=len(questions)
    )   
@app.route("/result")
def result():

    score = 0
    answers = session.get("answers", [])
    results = []

    for i in range(len(questions)):

        user_answer = answers[i]
        correct_answer = questions[i]["answer"]

        if user_answer == correct_answer:
            score += 1
            status = "correct"
        else:
            status = "wrong"

        results.append({
            "question": questions[i]["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "status": status
        })

    session.clear()

    return render_template(
        "result.html",
        score=score,
        total=len(questions),
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)