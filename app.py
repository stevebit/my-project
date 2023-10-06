import os
import openai
from fastcore.utils import nested_idx
from flask import Flask, request, render_template


openai.api_key = "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"

app = Flask(__name__, template_folder='C:\\\\Users\\\\steve\\\\OneDrive - Ageas Asia Services Limited\\\\Research\\\\webapp\\\\templates')

def askgpt(user, prev_msgs=None, system=None, model="gpt-4", **kwargs):
    msgs = []
    if prev_msgs:
        msgs.extend(prev_msgs)  # Include previous conversation history
    
    # Check if a system message already exists in the conversation history
    if system and not any(msg.get('role') == 'system' for msg in msgs):
        msgs.append({"role": "system", "content": system})
        
    msgs.append({"role": "user", "content": user})  # Add the new user message
    
    response = openai.ChatCompletion.create(model=model, messages=msgs, **kwargs)
    
    assistant_message = response['choices'][0]['message']['content']  # Extracting assistant's message from API response
    msgs.append({"role": "assistant", "content": assistant_message})  # Add the assistant's message to msgs
    
    return assistant_message, msgs  # Return the assistant's response and the updated message history

# Initialize an empty list to keep track of the conversation history
conversation_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global conversation_history  # Declare it as global to maintain state
    gpt_response = ""
    
    if request.method == 'POST':
        user_message = request.form['user_message']
        sys_role = "For the purposes of this conversation, please role-play as an insurance broker..."  # Your system role message

        gpt_response, conversation_history = askgpt(user=user_message, prev_msgs=conversation_history, system=sys_role)
    
    # Convert the conversation_history list of dictionaries to a string representation
    conversation_history_str = "\\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    
    return render_template("index.html", gpt_response=gpt_response, conversation_history=conversation_history)

if __name__ == "__main__":
    app.debug = True

app.run()



