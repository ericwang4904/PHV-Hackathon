from flask import Flask, render_template, request, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from src.cluster_model import cluster, cluster_df_to_dict
from src.llm_summary import cluster_summaries

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    question_text = db.Column(db.String(200))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_question', methods=['POST'])
def submit_question():
    if g.session_status:
        if request.method == 'POST':
            student_name = request.form['student_name']
            question_text = request.form['question_text']

            new_question = Question(student_name=student_name, question_text=question_text)
            db.session.add(new_question)
            db.session.commit()

    return redirect(url_for('student'))

@app.route('/empty_database', methods=['POST'])
def empty_database():
    if request.method == 'POST':
        Question.query.delete()
        db.session.commit()
    
    return redirect(url_for('admin'))

@app.route('/toggle_session', methods=['POST'])
def toggle_session():
    if request.method == 'POST':
        g.session_status = not (g.session_status)

    print(g.session_status)
    return redirect(url_for('admin'))

@app.route('/summary', methods=['POST'])
def summary():
        if request.method == 'POST':
            questions = [
                question.question_text for question in Question.query.all()
                ]
            
            if questions[0] == None:
                questions.pop(0)
        
            df = pd.DataFrame()
            df['sent'] = questions
            df = cluster(df, 1.2)
            cluster_dict = cluster_df_to_dict(df)
            summaries = cluster_summaries(cluster_dict)

            summary_text = ""
            for i,sum in enumerate(summaries):
                summary_text = summary_text + f"{i}. {sum}\n\n"

            g.summary_text = summary_text
            print(g.summary_text)

        return redirect(url_for('admin'))

@app.route('/admin')
def admin(): #choose when to start questions, when to end questions (then generate questions)
    return render_template('admin.html')

@app.route('/student')
def student():
    return render_template('student.html')
    
def setup():
    g.session_status = False
    g.summary_text = ""
    if not Question.query.first():
        db.session.add(Question())
        db.session.commit()

setup()

if __name__ == "__main__":
    app.run(debug=True)