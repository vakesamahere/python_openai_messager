from llm import send_llm_chat_request, Typewriter

# Simple non-streaming request
response = send_llm_chat_request(
    prompt="What is artificial intelligence?",
    temperature=0.7,
    max_tokens=1024,
    stream=False
)
print(response)

# Streaming request with typewriter effect
response = send_llm_chat_request(
    prompt="Tell me a short story",
    temperature=0.9,
    max_tokens=2048,
    stream=True,
    typewriter=Typewriter(delay=0.02)
)
print("\nComplete response:")
print(response)