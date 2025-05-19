import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json

# OpenRouter API Configuration
OPENROUTER_API_KEY = "*******"  # Replace with your OpenRouter API key
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-zero:free"  # Use the appropriate model

# Function to call OpenRouter API
def get_openrouter_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # Replace with your site URL
        "X-Title": "HealthBot",  # Optional: Replace with your site name
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        print("API Response Status Code:", response.status_code)  # Debugging
        print("API Response Content:", response.text)  # Debugging
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Sorry, I couldn't process your request. Status Code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Tkinter GUI for the Chatbot
class HealthBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HealthBot - Powered by OpenRouter")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25, state='disabled')
        self.chat_display.configure(font=("Arial", 12))
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input Field for Symptoms
        self.input_field = tk.Entry(root, width=70, font=("Arial", 12))
        self.input_field.grid(row=1, column=0, padx=10, pady=10)

        # Send Button
        self.send_button = tk.Button(root, text="Send", command=self.handle_input, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Start Button
        self.start_button = tk.Button(root, text="Start Diagnosis", command=self.start_diagnosis, bg="#2196F3", fg="white", font=("Arial", 12))
        self.start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Clear Button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_chat, bg="#9E9E9E", fg="white", font=("Arial", 12))
        self.clear_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Initialize conversation state
        self.conversation_history = []
        self.current_question = None

    # Function to display messages in the chat window
    def display_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)  # Auto-scroll to the bottom

    # Function to start the diagnosis process
    def start_diagnosis(self):
        self.conversation_history = []  # Reset conversation history
        self.display_message("Doctor", "Hello! I'm Dr. Dexter a General Physican at Akure Clinic. Please describe your symptoms or health concerns.")
        self.current_question = "What symptoms are you experiencing?"

    # Function to handle user input
    def handle_input(self):
        user_input = self.input_field.get().strip()
        if user_input:
            self.display_message("Patient", user_input)
            self.input_field.delete(0, tk.END)  # Clear the input field

            # Add the user's input to the conversation history
            self.conversation_history.append({"role": "user", "content": user_input})

            # Generate the doctor's response using OpenRouter API
            prompt = (
                "You are a doctor conducting a patient interview. "
                "keep your answer short and human like, meaning not more than 30 words"
                "The patient has described their symptoms. "
                "Ask one follow-up question at a time to gather more information. "
                "Here is the conversation so far:\n"
            )
            for entry in self.conversation_history:
                prompt += f"{entry['role']}: {entry['content']}\n"
            prompt += "Doctor:"

            bot_response = get_openrouter_response(prompt)
            bot_response = bot_response.replace("\\boxed{", "").replace("}", "")
            self.display_message("Doctor", bot_response)

            # Update the current question
            self.current_question = bot_response

    # Function to clear the chat 
    def clear_chat(self):
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        self.conversation_history = []
        self.current_question = None

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = HealthBotApp(root)
    root.mainloop()