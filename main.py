"""
AI Chatbot with Natural Language Processing
An intelligent chatbot that understands user queries and responds using NLP.
"""

import json
import random
import re
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
# from googlesearch import search  # Commented out due to Google blocking requests

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
                    "responses": ["I don't have access to the current time, but you can check your device's clock!", "I'm sorry, I don't have real-time clock access. What else can I help you with?"]
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
    
    def fetch_news(self, user_input):
        """Fetch latest news using NewsAPI"""
        text = user_input.lower()
        
        # Check for news keywords
        news_keywords = ['news', 'latest', 'headlines', 'breaking', 'updates']
        
        if any(keyword in text for keyword in news_keywords):
            try:
                # Extract news topic (remove news command)
                query = text
                for keyword in news_keywords:
                    query = query.replace(keyword, '').strip()
                
                # Remove common filler words
                filler_words = ['about', 'on', 'the', 'a', 'an', 'for', 'of']
                words = query.split()
                topic = ' '.join([word for word in words if word not in filler_words])
                
                # If no specific topic, use general news
                if not topic:
                    topic = 'general'
                
                # NewsAPI configuration
                # NOTE: Get your free API key from https://newsapi.org/
                api_key = os.getenv('NEWS_API_KEY', 'YOUR_NEWSAPI_KEY_HERE')
                
                if api_key == 'YOUR_NEWSAPI_KEY_HERE':
                    return "News feature requires NewsAPI key. Get one at https://newsapi.org/ and set NEWS_API_KEY environment variable."
                
                # Build NewsAPI URL
                base_url = 'https://newsapi.org/v2/everything'
                params = {
                    'q': topic,
                    'sortBy': 'publishedAt',
                    'language': 'en',
                    'pageSize': 3,
                    'apiKey': api_key
                }
                
                # Make request
                response = requests.get(base_url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('status') == 'ok' and data.get('articles'):
                    articles = data['articles']
                    
                    response_text = f"Latest news about '{topic}':\n\n"
                    for i, article in enumerate(articles, 1):
                        title = article.get('title', 'No title')
                        source = article.get('source', {}).get('name', 'Unknown source')
                        url = article.get('url', '')
                        
                        response_text += f"{i}. {title}\n"
                        response_text += f"   Source: {source}\n"
                        response_text += f"   Link: {url}\n\n"
                    
                    return response_text.strip()
                else:
                    return f"No news found for '{topic}'."
                    
            except requests.exceptions.RequestException as e:
                return f"Sorry, I couldn't fetch the news. Network error: {str(e)}"
            except Exception as e:
                return f"Sorry, I couldn't fetch the news. Error: {str(e)}"
        
        return None
    
    def search_web(self, user_input):
        """Detect and perform web searches"""
        text = user_input.lower()
        
        # Check for search keywords
        search_keywords = ['search', 'latest', 'news', 'find', 'look up', 'google']
        
        if any(keyword in text for keyword in search_keywords):
            try:
                # Extract search query (remove the search command)
                query = text
                for keyword in search_keywords:
                    query = query.replace(keyword, '').strip()
                
                # Remove common filler words
                filler_words = ['for', 'about', 'on', 'the', 'a', 'an']
                words = query.split()
                query = ' '.join([word for word in words if word not in filler_words])
                
                if not query:
                    return "Please specify what you'd like to search for."
                
                # Get search results (using mock for now)
                # Create proper Wikipedia URLs
                wiki_terms = {
                    'python': 'Python_(programming_language)',
                    'machine learning': 'Machine_learning',
                    'artificial intelligence': 'Artificial_intelligence',
                    'ai': 'Artificial_intelligence'
                }
                
                # Check if we have a known term, otherwise construct URL
                wiki_term = query.lower()
                if wiki_term in wiki_terms:
                    wiki_url = f"https://en.wikipedia.org/wiki/{wiki_terms[wiki_term]}"
                else:
                    # Title case and replace spaces with underscores
                    wiki_url = f"https://en.wikipedia.org/wiki/{query.title().replace(' ', '_')}"
                
                mock_results = [
                    wiki_url,
                    f"https://www.google.com/search?q={query.replace(' ', '+')}",
                    f"https://stackoverflow.com/search?q={query.replace(' ', '+')}"
                ]
                
                # Try to fetch content from the first result (Wikipedia)
                summary = None
                for url in mock_results[:2]:  # Try first two URLs
                    summary = self.fetch_page_summary(url, query)
                    if summary:
                        first_url = url
                        break
                
                if summary:
                    return f"Summary for '{query}':\n{summary}\n\nSource: {first_url}"
                else:
                    # Fallback to showing links
                    response = f"Here are the top search results for '{query}':\n"
                    for i, url in enumerate(mock_results, 1):
                        response += f"{i}. {url}\n"
                    return response.strip()
                    
            except Exception as e:
                return f"Sorry, I couldn't perform the search. Error: {str(e)}"
        
        return None
    
    def fetch_page_summary(self, url, query):
        """Fetch and summarize content from a webpage"""
        try:
            # Set a reasonable timeout and user agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # For Wikipedia, try to get the main content
            if 'wikipedia.org' in url:
                # Get the main content div
                content_div = soup.find('div', {'id': 'mw-content-text'})
                if content_div:
                    # Get the first few paragraphs
                    paragraphs = content_div.find_all('p', limit=3)
                    if paragraphs:
                        text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    else:
                        text = content_div.get_text()
                else:
                    text = soup.get_text()
            else:
                # For other sites, get general text
                text = soup.get_text()
            
            # Clean up the text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = ' '.join(lines)
            
            # Look for relevant content (first few sentences)
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip() and len(s) > 20]
            
            # Take first 2-3 relevant sentences
            summary_sentences = []
            for sentence in sentences[:3]:
                if len(' '.join(summary_sentences + [sentence])) < 400:  # Keep under 400 chars
                    summary_sentences.append(sentence)
                else:
                    break
            
            if summary_sentences:
                summary = '. '.join(summary_sentences) + '.'
                # Clean up extra whitespace
                summary = re.sub(r'\s+', ' ', summary)
                return summary
            
        except Exception as e:
            # Don't print error to avoid cluttering output
            return None
        
        return None
    
    def get_response(self, user_input):
        """Process user input and generate response"""
        # Check for news queries first
        news_result = self.fetch_news(user_input)
        if news_result:
            response = news_result
            intent_tag = "news"
        else:
            # Check for web search queries
            search_result = self.search_web(user_input)
            if search_result:
                response = search_result
                intent_tag = "search"
            else:
                # Check for math queries
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
