import tkinter as tk                      # Import core Tkinter GUI package
from tkinter import scrolledtext          # Import scrollable text widget
import time                               # For adding timestamps to messages
from symptom_bot import symptom_data, default_response, general_disclaimer, identify_symptoms
# Imports symptom matching logic and medicine data from separate module

# GUI class definition for MedBot
class MedBotGUI:
    def __init__(self, root):
        self.root = root                                 # Store root window
        self.root.title("MedBot")                        # Set window title
        self.root.geometry("700x500")                    # Set window size
        self.root.configure(bg="#000000")                # Set background to black for dark mode

        self.create_widgets()                            # Build all GUI components
        self.set_styles()                                # Apply styling (currently empty)

        # Show initial welcome message from the bot
        self.display_message("MedBot", 
            "👋 Hello! Describe your symptoms and I’ll suggest some medicines.\n\n"
            "⚠️ Not a substitute for professional medical advice."
        )

    # Create and place all UI widgets (chat box, input field, button)
    def create_widgets(self):
        # --- Chat display area (with scroll) ---
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Arial", 10),
            bg="#1a1a1a", fg="white", insertbackground="white"
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)       # Read-only by default

        # --- Input section (entry + send button) ---
        input_frame = tk.Frame(self.root, bg="#000000")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_box = tk.Entry(
            input_frame, font=("Arial", 10),
            bg="#1a1a1a", fg="white", insertbackground="white"
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_box.bind("<Return>", self.handle_send)  # Send on Enter key

        send_btn = tk.Button(
            input_frame, text="Send", command=self.handle_send,
            bg="#008080", fg="white"
        )
        send_btn.pack(side=tk.RIGHT)

    # (Optional) Apply tag styles for messages — currently not used
    def set_styles(self):
        pass

    # Display messages in chat box with timestamps
    def display_message(self, sender, message):
        timestamp = time.strftime("%H:%M")                        # Get current time
        self.chat_display.config(state=tk.NORMAL)                # Enable chat box for editing

        # Insert sender, time, and message
        self.chat_display.insert(tk.END, f"\n{sender} ({timestamp}):\n{message}\n")

        self.chat_display.see(tk.END)                            # Auto-scroll to bottom
        self.chat_display.config(state=tk.DISABLED)             # Make chat box read-only again

    # Triggered when Enter is pressed or Send button is clicked
    def handle_send(self, event=None):
        user_input = self.input_box.get().strip()                # Get text from input box

        if not user_input:
            return                                               # Don't do anything if input is empty

        self.input_box.delete(0, tk.END)                         # Clear input box
        self.display_message("You", user_input)                  # Show your message in chat

        # Simulate "Thinking..." with delay before bot replies
        self.root.after(500, lambda: self.display_message("MedBot", "Thinking..."))
        self.root.after(1500, lambda: self.respond(user_input))  # Wait 1.5s then respond

    # After delay, remove "Thinking..." and show the real response
    def respond(self, user_input):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", tk.END)               # Remove last 2 lines ("Thinking...")
        self.chat_display.config(state=tk.DISABLED)

        response = self.generate_response(user_input)            # Create a reply
        self.display_message("MedBot", response)                 # Show reply in chat

    # Core logic to build reply based on symptom input
    def generate_response(self, user_input):
        symptoms = identify_symptoms(user_input)                 # Match symptoms from input

        if not symptoms:                                         # If no known symptoms found
            return f"{default_response['message']}\n\n{default_response['disclaimer']}"

        response = "Based on your symptoms, here are suggestions:\n\n"

        for symptom in symptoms:
            data = symptom_data[symptom]                         # Get info from dataset
            response += f"{symptom.upper()}:\n{data['description']}\n\n"

            for med in data["medicines"]:                        # Loop through suggested medicines
                response += (
                    f"- {med['medicine']} (Dosage: {med['dosage']})\n"
                    f"  ⚠️ {med['warnings']}\n\n"
                )

            response += "-" * 40 + "\n"                          # Separator between symptoms

        response += general_disclaimer                           # Add general warning
        return response

# Main function to start the GUI application
if __name__ == "__main__":
    root = tk.Tk()            # Create main window
    MedBotGUI(root)           # Launch the MedBot GUI
    root.mainloop()           # Keep the app running
