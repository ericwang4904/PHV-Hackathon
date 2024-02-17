import requests

# Function to retrieve questions from the Flask backend
def get_questions():
    response = requests.get('http://127.0.0.1:5000/questions')
    if response.status_code == 200:
        questions = response.json()
        return questions
    else:
        return []

if __name__ == '__main__':
    questions = get_questions()
    print("Received questions:")
    for question in questions:
        print(question['text'])