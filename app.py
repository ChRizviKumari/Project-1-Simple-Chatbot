from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Greeting function
def greet_user():
    return "Hello! I'm your chatbot. How can I assist you today?"

# Responses to basic questions
responses = {
    "hi": "Hello",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "what is your name": "I'm called Chatbot. What's your name?",
    "what do you do basically": "I can chat with you, remember things from our conversation, and answer some basic questions.",
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "how is the weather": "I don't have access to real-time data, but I hope it's nice where you are!",
    "what's the time": "I don't have access to real-time information, so I can't tell you the time. Sorry!",
    "can you help me with something": "Of course! What do you need help with?",
    "what is your favorite color": "I'm a chatbot, so I don't have a favorite color. What's yours?",
    "do you like pizza": "I don't have taste buds, but I'm sure pizza is delicious!",
    "where are you from": "I exist in the digital world, so I don't have a physical location. I'm here to help you!"
}
user_name = None

def get_response(user_input):
    global user_name
    user_input_lower = user_input.lower()

    if "how are you" in user_input_lower:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "fine" in user_input_lower:
        return "Good to hear that! Can I help you with anything?"
    
    if "what is your name" in user_input_lower:
        return "I'm called Chatbot. What's your name?"
    elif user_name is None and "my name is" in user_input_lower:
        user_name = user_input[11:].capitalize()
        return "Ok"
    else:
        return responses.get(user_input_lower, "I don't understand that. Can you ask something else?")

# Farewell message
def say_goodbye():
    return "Goodbye! Have a great day!"

# Remember previous interactions
conversation_history = []

def remember_context(user_input):
    conversation_history.append(user_input)

def recall_context():
    return f"So far, you have said: {'; '.join(conversation_history)}"

# Error handling
def handle_error():
    return "I'm not sure I understand. Could you rephrase that?"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if user_input:
        if "bye" in user_input.lower():
            response = say_goodbye()
        elif "remember" in user_input.lower():
            remember_context(user_input)
            response = "Got it! I'll remember that."
        elif "recall" in user_input.lower():
            response = recall_context()
        else:
            response = get_response(user_input)
            if response == "I don't understand that. Can you ask something else?":
                response = handle_error()
            else:
                remember_context(user_input)
    else:
        response = handle_error()

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
