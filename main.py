import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(user_question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == user_question:
            return q["answer"]
    return None

def chatbot():
    knowledge_base = load_knowledge_base("knowledge_base.json")

    while True:
        user_input = input("Me: ")

        if user_input.lower() == 'quit':
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Genesis: {answer}')
        else:
            print('Bot: I don\'t know. Can you teach me?')
            new_answer = input('Type the answer or say "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print('Genesis: Thikhe Bhai, Aaj kuch naya sikha!')

if __name__ == '__main__':
    chatbot()
