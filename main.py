"""
AI Chatbot with Natural Language Processing
An intelligent chatbot that understands user queries and responds using NLP.
"""

import json
import random
import re
from datetime import datetime
import os

class NLProcessor:
    """Natural Language Processing engine for intent recognition"""
    
    def __init__(self, intents_path="intents.json"):
        self.intents = self.load_intents(intents_path)
        self.context = {}
        
    def load_intents(self, path):
        """Load intent definitions from JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_intents()
    
    def get_default_intents(self):
        """Default intents if file not found"""
        return {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
                    "responses": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Hey! Nice to see you!"]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["bye", "goodbye", "see you", "later"],
                    "responses": ["Goodbye! Have a great day!", "See you soon!", "Take care!"]
                },
                {
                    "tag": "help",
                    "patterns": ["help", "can you help", "what can you do", "assist"],
                    "responses": ["I can help you with: information, answering questions, and general conversation."]
                },
                {
                    "tag": "thanks",
                    "patterns": ["thank", "thanks", "appreciate"],
                    "responses": ["You're welcome!", "Happy to help!", "No problem!"]
                },
                {
                    "tag": "name",
                    "patterns": ["what is your name", "who are you", "your name"],
                    "responses": ["I'm an AI chatbot powered by Natural Language Processing.", "You can call me ChatBot!"]
                },
                {
                    "tag": "time",
                    "patterns": ["what time", "current time", "time now"],
                    "responses": []
                }
            ]
        }
    
    def preprocess(self, text):
        """Preprocess user input"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def tokenize(self, text):
        """Simple tokenization"""
        return text.split()
    
    def calculate_similarity(self, input_text, pattern):
        """Calculate word overlap similarity"""
        input_words = set(self.tokenize(self.preprocess(input_text)))
        pattern_words = set(self.tokenize(self.preprocess(pattern)))
        
        if not input_words or not pattern_words:
            return 0
            
        intersection = len(input_words & pattern_words)
        union = len(input_words | pattern_words)
        
        return intersection / union if union > 0 else 0
    
    def recognize_intent(self, user_input):
        """Recognize the intent from user input"""
        processed_input = self.preprocess(user_input)
        best_match = None
        highest_score = 0
        
        for intent in self.intents.get("intents", []):
            for pattern in intent.get("patterns", []):
                score = self.calculate_similarity(processed_input, pattern)
                if score > highest_score:
                    highest_score = score
                    best_match = intent
        
        # Special handling for time query
        if highest_score < 0.3:
            if any(word in processed_input for word in ['time', 'date', 'day']):
                return {
                    "tag": "time_query",
                    "response": f"Current time: {datetime.now().strftime('%I:%M %p')}",
                    "confidence": 0.8
                }
        
        if best_match and highest_score > 0.2:
            response = random.choice(best_match.get("responses", []))
            return {
                "tag": best_match.get("tag"),
                "response": response,
                "confidence": highest_score
            }
        
        return {
            "tag": "unknown",
            "response": "I'm not sure I understand. Could you rephrase that?",
            "confidence": 0.0
        }


class ChatBot:
    """Main chatbot class with conversation management"""
    
    def __init__(self, name="ChatBot"):
        self.name = name
        self.nlp = NLProcessor()
        self.conversation_history = []
        self.session_start = datetime.now()
    
    def solve_math(self, user_input):
        """Detect and solve math expressions"""
        # Convert word operators to symbols
        text = user_input.lower().replace('plus', '+').replace('minus', '-').replace('multiply', '*').replace('divided by', '/')
        
        # Check if it contains math pattern (numbers and operators)
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text):
            try:
                # Extract the entire math expression
                # Find sequences that contain numbers and operators
                expr_match = re.search(r'(\d+(?:\s*[\+\-\*\/]\s*\d+)+)', text)
                if expr_match:
                    expression = expr_match.group(1).replace(' ', '')  # Remove spaces
                    # Only allow safe characters
                    if re.match(r'^[\d\+\-\*\/\.]+$', expression):
                        result = eval(expression)
                        return f"The result is {result}"
            except:
                pass
        return None
    
    def get_response(self, user_input):
        """Process user input and generate response"""
        # Check for math queries first
        math_result = self.solve_math(user_input)
        if math_result:
            response = math_result
            intent_tag = "math"
        else:
            intent_result = self.nlp.recognize_intent(user_input)
            
            # Handle time-specific queries
            if intent_result["tag"] == "time_query":
                response = intent_result["response"]
            else:
                response = intent_result["response"]
            intent_tag = intent_result["tag"]
        
        # Store conversation
        self.conversation_history.append({
            "user": user_input,
            "bot": response,
            "intent": intent_tag,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def chat(self):
        """Interactive chat loop"""
        print(f"=== {self.name} - AI Chatbot ===")
        print("Type 'quit' or 'exit' to end the conversation\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"{self.name}: Goodbye! Have a great day!")
                    break
                    
                if not user_input:
                    continue
                    
                response = self.get_response(user_input)
                print(f"{self.name}: {response}")
                print()
                
            except KeyboardInterrupt:
                print(f"\n{self.name}: Goodbye!")
                break
            except EOFError:
                break
    
    def get_stats(self):
        """Get conversation statistics"""
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "total_messages": len(self.conversation_history),
            "intents_identified": list(set(msg["intent"] for msg in self.conversation_history))
        }


def main():
    """Main entry point"""
    chatbot = ChatBot("AI Assistant")
    chatbot.chat()
    
    # Show session stats
    stats = chatbot.get_stats()
    print("\n=== Session Statistics ===")
    print(f"Messages exchanged: {stats['total_messages']}")
    print(f"Session duration: {stats['session_duration']}")


if __name__ == "__main__":
    main()