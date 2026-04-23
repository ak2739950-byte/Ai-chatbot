"""
Enhanced AI Chatbot - ChatGPT-like Features
An intelligent chatbot with advanced NLP capabilities
"""

import json
import random
import re
from datetime import datetime
import os
import math

class EnhancedNLProcessor:
    """Advanced NLP engine with ChatGPT-like features"""
    
    def __init__(self, intents_path="intents.json"):
        self.intents = self.load_intents(intents_path)
        self.context = {}
        self.conversation_context = []
        
    def load_intents(self, path):
        """Load intent definitions from JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_intents()
    
    def get_default_intents(self):
        """Default intents if file not found"""
        return {"intents": []}
    
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
        
        for intent in self.get("intents", []):
            for pattern in intent.get("patterns", []):
                score = self.calculate_similarity(processed_input, pattern)
                if score > highest_score:
                    highest_score = score
                    best_match = intent
        
        # Check for special queries first
        if any(word in processed_input for word in ['calculate', 'compute', 'math', 'solve']):
            return self.handle_math_query(user_input)
        
        if any(word in processed_input for word in ['time', 'date', 'day']):
            return self.handle_time_query()
        
        if any(word in processed_input for word in ['write', 'code', 'program', 'function']):
            return self.handle_code_help(user_input)
        
        if best_match and highest_score > 0.2:
            response = random.choice(best_match.get("responses", []))
            return {
                "tag": best_match.get("tag"),
                "response": response,
                "confidence": highest_score
            }
        
        return {
            "tag": "unknown",
            "response": "I'm not sure I understand that. Could you rephrase?",
            "confidence": 0.0
        }
    
    def get(self, key, default=None):
        """Safe dictionary access"""
        return getattr(self, 'intents', {}).get(key, default)
    
    def handle_math_query(self, user_input):
        """Handle mathematical calculations"""
        try:
            # Extract numbers and operators
            numbers = re.findall(r'-?\d+\.?\d*', user_input)
            operators = re.findall(r'(plus|minus|multiply|divide|times|divided by|add|subtract|\+|\-|\*|/)', user_input.lower())
            
            if 'square root' in user_input.lower() or 'sqrt' in user_input.lower():
                if numbers:
                    n = float(numbers[0])
                    result = math.sqrt(n)
                    return {"tag": "math", "response": f"The square root of {n} is {result:.4f}", "confidence": 0.9}
            
            if 'power' in user_input.lower() or '^' in user_input:
                if len(numbers) >= 2:
                    result = float(numbers[0]) ** float(numbers[1])
                    return {"tag": "math", "response": f"{numbers[0]} raised to power {numbers[1]} = {result}", "confidence": 0.9}
            
            if numbers and len(numbers) >= 2:
                n1, n2 = float(numbers[0]), float(numbers[1])
                if any(op in user_input.lower() for op in ['plus', 'add', '+']):
                    return {"tag": "math", "response": f"{n1} + {n2} = {n1 + n2}", "confidence": 0.9}
                elif any(op in user_input.lower() for op in ['minus', 'subtract', '-']):
                    return {"tag": "math", "response": f"{n1} - {n2} = {n1 - n2}", "confidence": 0.9}
                elif any(op in user_input.lower() for op in ['multiply', 'times', '*']):
                    return {"tag": "math", "response": f"{n1} × {n2} = {n1 * n2}", "confidence": 0.9}
                elif any(op in user_input.lower() for op in ['divide', 'divided', '/']):
                    if n2 != 0:
                        return {"tag": "math", "response": f"{n1} ÷ {n2} = {n1 / n2:.4f}", "confidence": 0.9}
            
            # Try evaluating simple expressions
            expr = user_input.lower()
            for op, py_op in [('plus', '+'), ('minus', '-'), ('times', '*'), ('divide', '/')]:
                expr = expr.replace(op, py_op)
            expr = re.sub(r'[^\d+\-*/().]', '', expr)
            if expr:
                result = eval(expr)
                return {"tag": "math", "response": f"Result: {result}", "confidence": 0.9}
                
        except Exception as e:
            pass
        
        return {"tag": "math", "response": "I can help with calculations! Try 'calculate 5 plus 3' or 'square root of 16'", "confidence": 0.5}
    
    def handle_time_query(self):
        """Handle time and date queries"""
        now = datetime.now()
        return {
            "tag": "time",
            "response": f"Current time: {now.strftime('%I:%M %p')}\nDate: {now.strftime('%B %d, %Y')}\nDay: {now.strftime('%A')}",
            "confidence": 0.9
        }
    
    def handle_code_help(self, user_input):
        """Handle coding help requests"""
        code_topics = {
            'python': "Python is great for AI and data science! Key concepts:\n• Variables & Data Types\n• Lists, Dictionaries, Tuples\n• Functions & Classes\n• File Handling\n• Libraries: NumPy, Pandas, TensorFlow",
            'javascript': "JavaScript powers the web! Key topics:\n• Variables (let, const, var)\n• Functions & Arrow Functions\n• DOM Manipulation\n• Async/Await & Promises\n• Frameworks: React, Vue, Node.js",
            'java': "Java is enterprise-ready! Key concepts:\n• Object-Oriented Programming\n• Classes & Objects\n• Inheritance & Polymorphism\n• Collections Framework\n• Spring Framework",
            'html': "HTML builds web pages! Key elements:\n• <div>, <span>, <p>, <h1>-<h6>\n• <a> for links, <img> for images\n• <form>, <input>, <button>\n• Semantic tags: <header>, <nav>, <footer>",
            'css': "CSS styles web pages! Key topics:\n• Selectors (class, id, element)\n• Flexbox & Grid layouts\n• Animations & Transitions\n• Responsive design (@media)\n• CSS Frameworks: Bootstrap, Tailwind"
        }
        
        for lang, help_text in code_topics.items():
            if lang in user_input.lower():
                return {"tag": "code_help", "response": help_text, "confidence": 0.9}
        
        return {"tag": "code_help", "response": "I can help with code! Ask about Python, JavaScript, Java, HTML, or CSS. What would you like to learn?", "confidence": 0.7}


class EnhancedChatBot:
    """ChatGPT-like chatbot with advanced features"""
    
    def __init__(self, name="AI Assistant"):
        self.name = name
        self.nlp = EnhancedNLProcessor()
        self.conversation_history = []
        self.session_start = datetime.now()
        self.user_preferences = {}
        
    def get_response(self, user_input):
        """Process user input and generate response"""
        intent_result = self.nlp.recognize_intent(user_input)
        response = intent_result["response"]
        
        # Store conversation
        self.conversation_history.append({
            "user": user_input,
            "bot": response,
            "intent": intent_result["tag"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Update context
        self.nlp.conversation_context.append(user_input)
        
        return response
    
    def chat(self):
        """Interactive chat loop"""
        print("=" * 60)
        print("  🤖 Enhanced AI Chatbot - Like ChatGPT!")
        print("=" * 60)
        print("\nFeatures:")
        print("• Natural conversation")
        print("• Math calculations")
        print("• Code help")
        print("• Time & date")
        print("• And much more!\n")
        print("Type 'quit' or 'exit' to end | 'help' for commands\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{self.name}: Goodbye! Have a great day!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'clear':
                    self.conversation_history.clear()
                    print(f"\n{self.name}: Conversation cleared!")
                    continue
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                if user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if not user_input:
                    continue
                    
                response = self.get_response(user_input)
                print(f"{self.name}: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n{self.name}: Goodbye!")
                break
            except EOFError:
                break
    
    def show_help(self):
        """Show available commands"""
        print("""
📋 Available Commands:
• help    - Show this help message
• clear   - Clear conversation history
• history - Show conversation history
• stats   - Show session statistics
• quit    - Exit the chatbot

💡 Tips:
• Ask math questions: "calculate 5 + 3", "square root of 16"
• Get code help: "help with python", "javascript tutorial"
• Get time: "what time is it", "what day is it"
• Learn topics: AI, ML, Blockchain, IoT, etc.
""")
    
    def show_history(self):
        """Show conversation history"""
        print("\n📜 Conversation History:")
        for i, msg in enumerate(self.conversation_history[-10:], 1):
            print(f"{i}. You: {msg['user']}")
            print(f"   Bot: {msg['bot'][:100]}...")
            print()
    
    def show_stats(self):
        """Show session statistics"""
        stats = self.get_stats()
        print(f"""
📊 Session Statistics:
• Messages: {stats['total_messages']}
• Duration: {stats['session_duration']}
• Intents: {len(stats['intents_identified'])}
""")
    
    def get_stats(self):
        """Get conversation statistics"""
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "total_messages": len(self.conversation_history),
            "intents_identified": list(set(msg["intent"] for msg in self.conversation_history))
        }


def main():
    """Main entry point"""
    chatbot = EnhancedChatBot("AI Assistant")
    chatbot.chat()


if __name__ == "__main__":
    main()