"""Quick test to see chatbot output without interactive session"""

from main import ChatBot

# Create chatbot instance
bot = ChatBot("AI Assistant")

# Test queries
test_queries = [
    "hello",
    "what is your name",
    "help",
    "tell me a joke",
    "what is artificial intelligence",
    "what is nlp",
    "what time is it",
    "bye"
]

print("=== ChatBot Output Demo ===\n")

for query in test_queries:
    response = bot.get_response(query)
    print(f"You: {query}")
    print(f"Bot: {response}")
    print("-" * 40)