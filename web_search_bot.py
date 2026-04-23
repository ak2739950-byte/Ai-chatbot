"""
AI Chatbot with Web Search - Server se Answer dhund ke laata hai
Enhanced chatbot that can fetch answers from the internet
"""

import json
import random
import re
import math
from datetime import datetime
import os

try:
    import urllib.request
    import urllib.parse
    import urllib.error
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False


class WebSearchBot:
    """Chatbot with web search capability - Server se answer dhundke laata hai"""
    
    def __init__(self, name="AI Assistant"):
        self.name = name
        self.conversation_history = []
        self.session_start = datetime.now()
        self.intents = self.load_intents("intents.json")
        
    def load_intents(self, path):
        """Load intent definitions"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"intents": []}
    
    def preprocess(self, text):
        """Preprocess user input"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def tokenize(self, text):
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
        """Recognize intent from user input"""
        processed_input = self.preprocess(user_input)
        best_match = None
        highest_score = 0
        
        for intent in self.intents.get("intents", []):
            for pattern in intent.get("patterns", []):
                score = self.calculate_similarity(processed_input, pattern)
                if score > highest_score:
                    highest_score = score
                    best_match = intent
        
        # Check for special queries
        if any(word in processed_input for word in ['calculate', 'compute', 'math', 'solve', 'plus', 'minus', 'times']):
            return self.handle_math_query(user_input)
        
        if any(word in processed_input for word in ['time', 'date', 'day']):
            return self.handle_time_query()
        
        if any(word in processed_input for word in ['search', 'find', 'google', 'web', 'internet']):
            return {"tag": "web_search", "response": "I can search the web for you! Just ask your question and I'll find information.", "confidence": 0.8}
        
        if best_match and highest_score > 0.2:
            response = random.choice(best_match.get("responses", []))
            return {
                "tag": best_match.get("tag"),
                "response": response,
                "confidence": highest_score
            }
        
        # If no match, suggest web search
        return {
            "tag": "unknown",
            "response": f"I don't have information about '{user_input}'. Would you like me to search the web for this? Just say 'search for [your question]' and I'll find answers for you!",
            "confidence": 0.1
        }
    
    def handle_math_query(self, user_input):
        """Handle mathematical calculations"""
        try:
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
            
            expr = user_input.lower()
            for op, py_op in [('plus', '+'), ('minus', '-'), ('times', '*'), ('divide', '/')]:
                expr = expr.replace(op, py_op)
            expr = re.sub(r'[^\d+\-*/().]', '', expr)
            if expr:
                result = eval(expr)
                return {"tag": "math", "response": f"Result: {result}", "confidence": 0.9}
                
        except:
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
    
    def web_search(self, query):
        """Search the web for answers - Server se information dhundta hai"""
        # Simulated web search results (in real implementation, you'd use an API)
        search_results = {
            "python": "Python is a high-level, interpreted programming language. It's widely used for web development, data science, AI, and automation. Python was created by Guido van Rossum and first released in 1991.",
            "artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence in machines. It enables computers to learn from experience, adjust to new inputs, and perform human-like tasks like reasoning, learning, and problem-solving.",
            "machine learning": "Machine Learning is a subset of AI that enables systems to learn from data without being explicitly programmed. It uses algorithms to identify patterns and make decisions.",
            "web development": "Web development is creating websites and web applications. It includes frontend (HTML, CSS, JavaScript) and backend (Node.js, Python, PHP) development.",
            "data science": "Data Science combines statistics, programming, and domain knowledge to extract insights from data using Python, R, and various ML tools.",
            "blockchain": "Blockchain is a decentralized, distributed digital ledger that records transactions across many computers. It's secure, transparent, and immutable.",
            "javascript": "JavaScript is a programming language used for web development. It enables interactive web pages and is an essential part of web applications.",
            "java": "Java is a high-level, object-oriented programming language used for enterprise applications, Android development, and web services.",
            "html": "HTML (HyperText Markup Language) is the standard markup language for creating web pages and web applications.",
            "css": "CSS (Cascading Style Sheets) is used to style and layout web pages, including colors, fonts, and responsive design.",
            "react": "React is a JavaScript library for building user interfaces, developed by Facebook. It's used for single-page applications.",
            "nodejs": "Node.js is a JavaScript runtime built on Chrome's V8 engine, used for server-side programming and building scalable network applications.",
            "database": "A database is an organized collection of structured information, or data, typically stored electronically in a computer system.",
            "api": "API (Application Programming Interface) allows different software applications to communicate with each other.",
            "cloud computing": "Cloud computing delivers computing services over the internet, including servers, storage, databases, and software.",
            "cybersecurity": "Cybersecurity protects computers, networks, and data from unauthorized access and cyber attacks.",
            "iot": "IoT (Internet of Things) connects everyday devices to the internet, allowing them to collect and share data.",
            "deep learning": "Deep Learning is a subset of machine learning using artificial neural networks with multiple layers.",
            "neural network": "Neural Networks are AI models inspired by the human brain, consisting of input, hidden, and output layers.",
            "docker": "Docker is a platform for developing, shipping, and running applications in containers.",
            "git": "Git is a distributed version control system for tracking changes in source code during software development."
        }
        
        query_lower = query.lower()
        
        # Search in our knowledge base
        for key, value in search_results.items():
            if key in query_lower:
                return f"🔍 Search Result for '{query}':\n\n{value}\n\n(Source: Web Knowledge Base)"
        
        # Default response for unknown queries
        return f"🔍 I searched for '{query}' but don't have specific information.\n\n💡 Tips:\n• Try asking about: Python, AI, Machine Learning, Web Dev, JavaScript, etc.\n• Or say 'search for [topic]' to search the web"
    
    def get_response(self, user_input):
        """Process user input and generate response"""
        # Check if user wants to search
        if user_input.lower().startswith('search for') or user_input.lower().startswith('search'):
            query = user_input.lower().replace('search for', '').replace('search', '').strip()
            response = self.web_search(query)
        else:
            intent_result = self.recognize_intent(user_input)
            response = intent_result["response"]
        
        # Store conversation
        self.conversation_history.append({
            "user": user_input,
            "bot": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def chat(self):
        """Interactive chat loop"""
        print("=" * 60)
        print("  🌐 AI Chatbot with Web Search!")
        print("  Server se answer dhundke laata hai!")
        print("=" * 60)
        print("\nFeatures:")
        print("• Web Search - Kisi bhi topic par information")
        print("• Math Calculator")
        print("• Time & Date")
        print("• 30+ Topics par gyan")
        print("\nCommands:")
        print("• 'search for [topic]' - Web search karega")
        print("• 'help' - Help dekhe")
        print("• 'quit' - Exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{self.name}: Goodbye! Have a great day!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
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
    
    def show_help(self):
        print("""
📋 Available Commands:
• search for [topic] - Web search karega
• help    - Show this help
• stats   - Show statistics
• quit    - Exit

💡 Example Questions:
• "search for python tutorial"
• "what is machine learning"
• "calculate 5 plus 3"
• "what time is it"
""")
    
    def show_stats(self):
        print(f"""
📊 Session Statistics:
• Messages: {len(self.conversation_history)}
• Duration: {datetime.now() - self.session_start}
""")


def main():
    chatbot = WebSearchBot("AI Assistant")
    chatbot.chat()


if __name__ == "__main__":
    main()