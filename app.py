from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app=Flask(__name__)
app.debug = True
app.config['SECRET_KEY']='super-secret-key'
debug = DebugToolbarExtension(app)
responses=[]
user_question = -1

@app.route('/')
def start_page():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def question_page(qid):
    if len(responses) != qid:
        flash("Please start from the start page")
        return redirect('/')
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', survey = satisfaction_survey, question = question )

@app.route('/answer', methods = ['POST'])
def answer_handler():
    answer=request.form['answer']
    responses.append(answer)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    return redirect(f'/questions/{len(responses)}')

@app.route('/thank-you')
def thank_user():
    return render_template('thank-you.html', survey=satisfaction_survey)