import requests
import random
import html

EDUCATION_CATEGORY_ID = 9 
API_URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def get_education_questions():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
    
        if data['response_code'] == 0 and data['results']:
            return data['results']
    return None

def run_quiz():
    """Runs the main quiz loop, manages questions, input, and scoring."""
    questions = get_education_questions()
    if not questions:
        print("Failed to fetch educational questions. Please check your network connection and API URL.")
        return
    score = 0
    print("Welcome to the Education Quiz!\n")

    for i, q in enumerate(questions, 1):
        question = html.unescape(q['question'])
        correct = html.unescape(q['correct_answer'])
        incorrects = [html.unescape(a) for a in q['incorrect_answers']]

        options = incorrects + [correct]
        random.shuffle(options)

        print(f"---")
        print(f"Question {i}: {question}")
        for idx, option in enumerate(options, 1):
            print(f" {idx}. {option}")

        while True:
            try:

                choice = int(input("\nYour answer (1-4): "))
               
                if 1 <= choice <= 4:
                    break
                else:
                    print("Invalid input! Please enter 1, 2, 3, or 4.")
            except ValueError:

                pass
            
            print("Invalid input! Please enter 1, 2, 3, or 4.")

        if options[choice-1] == correct:
            print("✓ Correct!\n")
            score += 1
        else:
            print(f"X Wrong! The correct answer was: {correct}\n")

    print("=============================")
    print("Quiz Complete!")
    print(f"Final Score: {score}/{len(questions)}")

    if questions:
        percentage = (score / len(questions)) * 100
        print(f"Percentage: {percentage:.1f}%")
    print("=============================")
if __name__ == "__main__":
    run_quiz()