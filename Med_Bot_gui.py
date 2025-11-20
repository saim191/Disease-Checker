import tkinter as tk
from tkinter import scrolledtext
import time
from symptom_bot import symptom_data, default_response, general_disclaimer, identify_symptoms

class MedBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MedBot")
        self.root.geometry("700x500")
        self.root.configure(bg="#000000")

        self.create_widgets()
        self.set_styles()

        self.display_message("MedBot", 
            "👋 Hello! Describe your symptoms and I’ll suggest some medicines.\n\n"
            "⚠️ Not a substitute for professional medical advice."
        )

    def create_widgets(self):
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Arial", 10),
            bg="#1a1a1a", fg="white", insertbackground="white"
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        input_frame = tk.Frame(self.root, bg="#000000")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_box = tk.Entry(
            input_frame, font=("Arial", 10),
            bg="#1a1a1a", fg="white", insertbackground="white"
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_box.bind("<Return>", self.handle_send)

        send_btn = tk.Button(
            input_frame, text="Send", command=self.handle_send,
            bg="#008080", fg="white"
        )
        send_btn.pack(side=tk.RIGHT)

    def set_styles(self):
        pass

    def display_message(self, sender, message):
        timestamp = time.strftime("%H:%M")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender} ({timestamp}):\n{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def handle_send(self, event=None):
        user_input = self.input_box.get().strip()

        if not user_input:
            return

        self.input_box.delete(0, tk.END)
        self.display_message("You", user_input)

        self.root.after(500, lambda: self.display_message("MedBot", "Thinking..."))
        self.root.after(1500, lambda: self.respond(user_input))

    def respond(self, user_input):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", tk.END)
        self.chat_display.config(state=tk.DISABLED)

        response = self.generate_response(user_input)
        self.display_message("MedBot", response)

    def generate_response(self, user_input):
        symptoms = identify_symptoms(user_input)

        if not symptoms:
            return f"{default_response['message']}\n\n{default_response['disclaimer']}"

        response = "Based on your symptoms, here are suggestions:\n\n"

        for symptom in symptoms:
            data = symptom_data[symptom]
            response += f"{symptom.upper()}:\n{data['description']}\n\n"

            for med in data["medicines"]:
                response += (
                    f"- {med['medicine']} (Dosage: {med['dosage']})\n"
                    f"  ⚠️ {med['warnings']}\n\n"
                )

            response += "-" * 40 + "\n"

        response += general_disclaimer
        return response

if __name__ == "__main__":
    root = tk.Tk()
    MedBotGUI(root)
    root.mainloop()
