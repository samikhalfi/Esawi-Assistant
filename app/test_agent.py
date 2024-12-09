import sys
from pathlib import Path
import asyncio

# Add the project root directory to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.chat import AIThinkingAssistant

# Initialize the AI assistant
ai_assistant = AIThinkingAssistant()

# Function to test the chatbot interactively and with test cases
async def test_chatbot():
    print("AI Assistant Test Mode")
    print("Type 'exit' to quit.")
    
    # Predefined test cases
    test_cases = [
        "What is the capital of France?",
        "Can you explain quantum mechanics in simple terms?",
        "Generate a short story about a robot in space.",
        "Solve this math problem: 2x + 3 = 9.",
        "How can I improve my Python programming skills?",
        "What are the key principles of machine learning?",
        "Tell me a joke!",
        "Translate 'Good morning' to French.",
    ]
    
    print("\n--- Running predefined test cases ---\n")
    for idx, test_case in enumerate(test_cases, start=1):
        print(f"Test {idx}: {test_case}")
        response = await ai_assistant.generate_response(test_case)
        print(f"AI: {response}\n")
    
    print("--- Predefined test cases completed ---\n")
    
    # Interactive mode
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting. Goodbye!")
            break

        # Generate response
        try:
            response = await ai_assistant.generate_response(user_input)
            print(f"AI: {response}")
        except Exception as e:
            print(f"Error: {e}")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_chatbot())
