from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

SECURITY_KEY = "ligma"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    question_text = db.Column(db.String(200))
    importance = db.Column(db.Integer)

    def __repr__(self):
        return f"<Question {self.id}>"

@app.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/submit_question', methods=['POST'])
def submit_question():
    if request.method == 'POST':
        student_name = request.form['student_name']
        question_text = request.form['question_text']
        importance = int(request.form['importance'])
        new_question = Question(student_name=student_name, question_text=question_text, importance=importance)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/empty_database', methods=['POST'])
def empty_database():
    if request.method == 'POST':
        Question.query.delete()
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/toggle_session', methods=['POST'])
def toggle_session():
    if request.method == 'POST':
        # Logic to toggle session
        return redirect(url_for('index'))

@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        # Logic to generate summary
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

    
@app.route('/admin')
def admin(key=None): #choose when to start questions, when to end questions (then generate questions)
    print(key)
    if key != SECURITY_KEY:
        return 'Unauthorized', 401
    

# Hard bits:
# 1. student can't send when admin turns of sending 
# 2. summarizing should only be run once per question cycle
# 3. 
# 