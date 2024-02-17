
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    sender = db.Column(db.String(30), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit_question():
    data = request.get_json()
    text = data.get('text')
    if text:
        question = Question(text=text, id=id, sender=sender)
        db.session.add(question)
        db.session.commit()
        return jsonify({'message': 'Question submitted successfully'})
    else:
        return jsonify({'error': 'Text field is required'}), 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
