import json
import difflib
from difflib import get_close_matches
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ttkbootstrap as ttk

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        return {"questions": []}

def save_knowledge_base(file_path:str, knowledge_base: dict):
    with open(file_path, 'w') as file:
        json.dump(knowledge_base, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

def chat_bot(user_input: str, knowledge_base: dict, output_text: tk.Text):
    if user_input.lower() == 'quit':
        return "quit"

    best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer: str = get_answer_for_question(best_match, knowledge_base)
        output_text.insert(tk.END, f'You: {user_input}\n')
        output_text.insert(tk.END, f'Bot: {answer}\n\n')
    else:
        output_text.insert(tk.END, f'You: {user_input}\n')
        output_text.insert(tk.END, f'Bot: I don\'t know the answer. Do you want to teach me?\n\n')
        teach_new_answer(user_input, knowledge_base, output_text)

def teach_new_answer(user_input: str, knowledge_base: dict, output_text: tk.Text):
    answer = messagebox.askquestion("Teach Me", "I don't know the answer. Do you want to teach me?")
    if answer == 'yes':
        new_answer = simpledialog.askstring("Teach Me", "Enter the answer:")
        if new_answer:
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            messagebox.showinfo("Teach Me", "Thank you! I learned a new response!")
            output_text.insert(tk.END, f'You: {user_input}\n')
            output_text.insert(tk.END, f'Bot: {new_answer}\n\n')
        else:
            output_text.insert(tk.END, f'You: {user_input}\n')
            output_text.insert(tk.END, f'Bot: Please provide a valid answer.\n\n')

def on_send_click(entry_field: tk.Entry, knowledge_base: dict, output_text: tk.Text):
    user_input = entry_field.get().strip()
    entry_field.delete(0, tk.END)

    if user_input:
        action = chat_bot(user_input, knowledge_base, output_text)
        if action == "quit":
            root.quit()

def main():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    root = ttk.Window(themename = 'darkly') 
    root.title("Chatbot")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    entry_field = ttk.Entry(main_frame, width=40)
    entry_field.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

    send_button = ttk.Button(main_frame, text="Send", command=lambda: on_send_click(entry_field, knowledge_base, output_text))
    send_button.grid(row=0, column=1, padx=5, pady=5)

    output_text = tk.Text(main_frame, wrap="word", width=60, height=20)
    output_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

    root.mainloop()

if __name__ == '__main__':
    main()
