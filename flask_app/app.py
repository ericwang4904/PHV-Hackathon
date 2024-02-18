from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from src.cluster_model import cluster, cluster_df_to_dict
from src.llm_summary import cluster_summaries

def create_app():
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
        if app.session_status:
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
            if app.session_status:
                app.session_status=False
            else:
                app.session_status=True


        print(app.session_status)
        return redirect(url_for('admin'))

    @app.route('/summary', methods=['POST'])
    def summary():
            if request.method == 'POST':
                questions = [
                    question.question_text for question in Question.query.all()
                    ]
                
                if len(questions) == 0:
                    return redirect(url_for('admin'))
                if questions[0] == None:
                    questions.pop(0)
            
                df = pd.DataFrame()
                df['sent'] = questions
                df = cluster(df, 1.2)
                cluster_dict = cluster_df_to_dict(df)
                app.cluster_dict = cluster_dict
                summaries = cluster_summaries(cluster_dict)

                summary_text = []
                for i,sum in enumerate(summaries):
                    summary_text.append(f"{i+1}. {sum} (Num Questions: {len(cluster_dict[i])})")
                
                print(cluster_dict)

                app.summary_text = summary_text

            return redirect(url_for('admin'))

    @app.route('/admin')
    def admin(): #choose when to start questions, when to end questions (then generate questions)
        return render_template('admin.html', session_status=app.session_status, summary_text=app.summary_text)

    @app.route('/student')
    def student():
        return render_template('student.html', session_status=app.session_status)
    
    @app.route('/question_clusters')
    def question_clusters():
        return render_template('question_clusters.html', cluster_dict=app.cluster_dict)
    
    with app.app_context():
        if not Question.query.first():
            db.session.add(Question())
            db.session.commit()

        app.session_status = True
        app.cluster_dict = [[
                    question.question_text for question in Question.query.all()
                    ]]
        app.summary_text = []


    return app