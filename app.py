from flask import Flask, render_template, request
from datetime import datetime
import csv
import os
from botRespond import getResponse

app = Flask(__name__)

# Constants
CHATBOT_NAME = 'Alumni Bot'
LOG_FILE_PATH = 'data/log.csv'

# Ensure the 'data' directory exists
os.makedirs('data', exist_ok=True)

# Function to log chat to CSV file
def log_to_csv(user_text, bot_reply):
    file_exists = os.path.isfile(LOG_FILE_PATH)
    
    with open(LOG_FILE_PATH, 'a', newline='') as logFile:
        writer = csv.writer(logFile)
        if not file_exists:
            # Write headers if the file is being created for the first time
            writer.writerow(['User Input', 'Bot Response'])
        writer.writerow([user_text, bot_reply])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    bot_reply = str(getResponse(user_text))
    
    # Handle special bot responses
    if bot_reply == "IDKresponse":
        bot_reply = str(getResponse('IDKnull'))
    elif bot_reply == "getTIME":
        bot_reply = datetime.now().strftime("%H:%M:%S")  # Current time
    elif bot_reply == "getDATE":
        bot_reply = datetime.now().strftime("%Y-%m-%d")  # Current date
    
    # Log conversation
    log_to_csv(user_text, bot_reply)

    return bot_reply

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

