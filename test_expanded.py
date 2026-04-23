"""Test expanded chatbot knowledge"""

from main import ChatBot

bot = ChatBot()

# Test various topics
test_queries = [
    "what is python",
    "what is machine learning", 
    "what is blockchain",
    "what is iot",
    "what is quantum computing",
    "motivate me",
    "what is neural network",
    "what is computer vision"
]

print("=" * 60)
print("EXPANDED CHATBOT KNOWLEDGE BASE")
print("=" * 60)

for query in test_queries:
    response = bot.get_response(query)
    print(f"\n❓ Question: {query}")
    print(f"🤖 Answer: {response}")
    print("-" * 60)