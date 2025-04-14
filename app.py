import tkinter as tk
from tkinter import messagebox
import threading
from chatBot import ChatBot  # Import the ChatBot class from the chatBot.py file

# Create an instance of ChatBot
#api_key = ""
chatbot = ChatBot(api_key)

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")

        # Set window size (larger window for better spacing)
        self.root.geometry("500x700")

        # Set background color to dark grey
        self.root.configure(bg="#2e2e2e")

        # Flag to control whether chat should continue
        self.stop_chat = False

        self.chat_thread = None

        # Home screen - show buttons to navigate
        self.home_screen()

    def home_screen(self):
        # Clear the window (if any widgets are present)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a label for the home screen
        home_label = tk.Label(self.root, text="AI Chat Buddy", font=("Arial", 24, "bold"), fg="white", bg="#2e2e2e")
        home_label.pack(pady=50)

        # Create a button to go to the chatbot interface (does not start chat)
        go_to_chat_button = tk.Button(self.root, text="New Chat", command=self.go_to_chat_screen, font=("Arial", 16, "bold"), bg="#555555", fg="white", width=20, height=2)
        go_to_chat_button.pack(pady=10)

        # Placeholder buttons for future features (buttons will do nothing for now)
        placeholder_button_1 = tk.Button(self.root, text="Feature 1 (To be implemented)", state=tk.DISABLED, font=("Arial", 16, "bold"), bg="#555555", fg="white", width=20, height=2)
        placeholder_button_1.pack(pady=10)

        placeholder_button_2 = tk.Button(self.root, text="Feature 2 (To be implemented)", state=tk.DISABLED, font=("Arial", 16, "bold"), bg="#555555", fg="white", width=20, height=2)
        placeholder_button_2.pack(pady=10)

        placeholder_button_3 = tk.Button(self.root, text="Feature 3 (To be implemented)", state=tk.DISABLED, font=("Arial", 16, "bold"), bg="#555555", fg="white", width=20, height=2)
        placeholder_button_3.pack(pady=10)

    def go_to_chat_screen(self):
        # Clear the home screen and start the chat interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame for the back button at the top
        back_button_frame = tk.Frame(self.root, bg="#2e2e2e", height=40)  # Added height to frame
        back_button_frame.pack(fill=tk.X, pady=(10, 20))  # Add padding between top of window and back button

        # Create a Back button in the top-left corner to go back to the home screen
        back_button = tk.Button(back_button_frame, text="Back", command=self.home_screen, font=("Arial", 12, "bold"), bg="#555555", fg="white", width=8, height=1)
        back_button.place(x=10, y=5)  # Position the button at the top-left corner with some vertical space

        # Create a text area to display the conversation
        self.text_area = tk.Text(self.root, state=tk.DISABLED, wrap=tk.WORD, bg="#333333", fg="white", font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Padding added to prevent overlap

        # Create an entry field for user input
        self.entry_field = tk.Entry(self.root, font=("Arial", 14))
        self.entry_field.pack(padx=10, pady=10, fill=tk.X)

        # Bind the enter key to send input
        self.entry_field.bind("<Return>", self.handle_user_input)

        # Create a button to start the conversation
        self.start_button = tk.Button(self.root, text="Start Chat", command=self.start_chat, font=("Arial", 14), bg="#555555", fg="white", width=20, height=2)
        self.start_button.pack(pady=10)


    def start_chat(self):
        # Set stop_chat flag to False when chat starts
        self.stop_chat = False
        if self.chat_thread is None or not self.chat_thread.is_alive():
            # Start the chat in a new thread to keep the UI responsive
            self.chat_thread = threading.Thread(target=self.run_chat)
            self.chat_thread.daemon = True  # Ensures the thread exits when the main program exits
            self.chat_thread.start()

    def run_chat(self):
        # Initialize conversation history
        message_history = []
        self.is_chatting = True  # Flag to track chat continuation

        # Inform the user that the chatbot is listening
        self.update_text_area("ChatBot: I'm ready to chat!\n")

        while not self.stop_chat:

            user_input = chatbot.speechToText("English")  # Get speech input from user

            if user_input.lower() == "quit" or user_input.lower() == "exit":
                self.stop_chat = True  # Set flag to stop chat
                self.update_text_area("ChatBot: Ending chat...\n")
                break

            self.update_text_area(f"You: {user_input}\n")

            # Add user message to the conversation history
            message_history.append({"role": "user", "content": user_input})

            # Get chatbot's response
            completion = chatbot.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message_history
            )
            bot_response = completion.choices[0].message.content

            self.update_text_area(f"ChatBot: {bot_response}\n")
            chatbot.textToSpeech(bot_response, "English", "indifferent")  # Convert bot's response to speech

    def handle_user_input(self, event=None):
        # Get user input from the entry field
        user_input = self.entry_field.get()

        if user_input.lower() == "quit" or user_input.lower() == "exit":
            self.stop_chat = True  # Set stop_chat flag
            self.update_text_area("Ending chat...\n")
            return

        # Display user input in the text area
        self.update_text_area(f"You: {user_input}\n")
        self.entry_field.delete(0, tk.END)

        # Process the input and get bot's response in a new thread
        self.get_bot_response(user_input)

    def get_bot_response(self, user_input):
        # Here, we handle the conversation logic between the user and bot
        message_history = [{"role": "user", "content": user_input}]
        bot_response = chatbot.generateMessage(message_history)
        self.update_text_area(f"ChatBot: {bot_response}\n")
        chatbot.textToSpeech(bot_response, "English", "indifferent")  # Convert bot's response to speech

    def update_text_area(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)

# Create and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


















################################################################################

# from flask import Flask, render_template, url_for

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(debug=True) #set debug to false in production

################################################################################

# import tkinter

# Tk(screenName=None,  baseName=None,  className='Chatbot',  useTk=1)

# from tkinter import *
# from tkinter.ttk import *
# from time import strftime

# def buttonPressed(screen, buttonName):
#     if (buttonName == "lets talk"):
#         screen.configure(bg = "green")


# m = Tk()
# m.title("Chatbot!")
# m.minsize(500, 500)
# m.configure(bg = "gray")

# Button(m, text = "Let's talk!", command=lambda: buttonPressed(m, "lets talk")).pack(side = TOP, pady = 10)

# mainloop()

################################################################################

# from tkinter import *
# from tkinter.ttk import *
# from time import strftime
 
# # creating tkinter window
# root = Tk()
 
# # setting the minimum size of the root window
# root.minsize(150, 100)
 
# # Adding widgets to the root window
# Label(root, text = 'GeeksforGeeks', 
#       font =('Verdana', 15)).pack(side = TOP, pady = 10)
# Button(root, text = 'Click Me !').pack(side = TOP)

# mainloop()

################################################################################


################################################################################

# import tkinter as tk

# class RobotFace:
#     def __init__(self, root):
#         self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
#         self.canvas.pack()

#         # Create buttons to change expressions
#         btn_frame = tk.Frame(root)
#         btn_frame.pack()
#         tk.Button(btn_frame, text="Happy", command=self.draw_happy).pack(side=tk.LEFT)
#         tk.Button(btn_frame, text="Serious", command=self.draw_serious).pack(side=tk.LEFT)
#         tk.Button(btn_frame, text="Angry", command=self.draw_angry).pack(side=tk.LEFT)
#         tk.Button(btn_frame, text="Sad", command=self.draw_sad).pack(side=tk.LEFT)

#         self.draw_happy()  # Start with happy face

#     def draw_face_base(self):
#         # Clear the canvas
#         self.canvas.delete("all")
        
#         # Draw the face outline
#         self.canvas.create_oval(100, 100, 300, 300, outline="black", fill="#d3d3d3")  # Face

#         # Eyes (base position)
#         self.left_eye = self.canvas.create_oval(140, 150, 180, 190, fill="white")
#         self.right_eye = self.canvas.create_oval(220, 150, 260, 190, fill="white")

#     def draw_happy(self):
#         self.draw_face_base()

#         # Happy mouth
#         self.canvas.create_arc(150, 200, 250, 260, start=0, extent=-180, style=tk.ARC, width=3)

#         # Happy eyebrows (raised)
#         self.canvas.create_line(135, 140, 180, 130, width=3)  # Left eyebrow
#         self.canvas.create_line(220, 130, 265, 140, width=3)  # Right eyebrow

#     def draw_serious(self):
#         self.draw_face_base()

#         # Serious mouth (straight line)
#         self.canvas.create_line(150, 240, 250, 240, width=3)

#         # Neutral eyebrows (straight)
#         self.canvas.create_line(135, 140, 180, 140, width=3)  # Left eyebrow
#         self.canvas.create_line(220, 140, 265, 140, width=3)  # Right eyebrow

#     def draw_angry(self):
#         self.draw_face_base()

#         # Angry mouth
#         self.canvas.create_arc(150, 230, 250, 270, start=0, extent=180, style=tk.ARC, width=3)

#         # Angry eyebrows (angled down)
#         self.canvas.create_line(135, 140, 180, 150, width=3)  # Left eyebrow
#         self.canvas.create_line(220, 150, 265, 140, width=3)  # Right eyebrow

#     def draw_sad(self):
#         self.draw_face_base()

#         # Sad mouth
#         self.canvas.create_arc(150, 240, 250, 280, start=0, extent=180, style=tk.ARC, width=3)

#         # Sad eyebrows (angled up)
#         self.canvas.create_line(135, 150, 180, 140, width=3)  # Left eyebrow
#         self.canvas.create_line(220, 140, 265, 150, width=3)  # Right eyebrow

# # Create the main application window
# root = tk.Tk()
# root.title("Simple Robot Face")

# # Create the RobotFace instance
# robot_face = RobotFace(root)

# # Start the Tkinter main loop
# root.mainloop()
