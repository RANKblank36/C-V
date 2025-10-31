import requests
import random
import html
import time

def fetch_questions(amount=5):
    """Fetch trivia questions from the Open Trivia Database API."""
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    response = requests.get(url)
    data = response.json()
    return data["results"]

def display_question(question_data, q_num):
    """Display a single question and its answer options."""
    question = html.unescape(question_data["question"])
    correct_answer = html.unescape(question_data["correct_answer"])
    incorrect_answers = [html.unescape(ans) for ans in question_data["incorrect_answers"]]
    
    options = incorrect_answers + [correct_answer]
    random.shuffle(options)
    
    print(f"\nQuestion {q_num}: {question}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    # Get user's answer
    while True:
        try:
            answer = int(input("Your answer (1-4): "))
            if 1 <= answer <= 4:
                break
            else:
                print("❌ Please enter a number between 1 and 4.")
        except ValueError:
            print("❌ Invalid input. Please enter a number between 1 and 4.")
    
    # Check answer
    if options[answer - 1] == correct_answer:
        print("✅ Correct!")
        return True
    else:
        print(f"❌ Wrong! The correct answer was: {correct_answer}")
        return False

def trivia_quiz():
    print("🎯 Welcome to the Trivia Quiz!\n")
    questions = fetch_questions()
    score = 0

    for i, question_data in enumerate(questions, 1):
        start_time = time.time()
        correct = display_question(question_data, i)
        end_time = time.time()

        if end_time - start_time > 10:
            print("⏰ Time’s up! That question won’t count.")
        elif correct:
            score += 1

    print(f"\n🏁 Quiz Complete! Your final score: {score}/{len(questions)}")

if __name__ == "__main__":
    trivia_quiz()
