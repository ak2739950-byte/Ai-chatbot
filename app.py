"""
Web Dashboard for AI Chatbot
A simple web interface to interact with the chatbot
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ChatBot

app = Flask(__name__)
chatbot = ChatBot("AI Assistant")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if user_message.lower() in ['quit', 'exit', 'bye']:
        return jsonify({'response': 'Goodbye! Have a great day!', 'done': True})
    
    response = chatbot.get_response(user_message)
    return jsonify({'response': response})

@app.route('/stats')
def stats():
    stats_data = chatbot.get_stats()
    return jsonify(stats_data)

if __name__ == '__main__':
    print("=" * 50)
    print("  AI Chatbot Dashboard")
    print("  Open browser at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)