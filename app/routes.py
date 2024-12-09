from flask import Flask, render_template, request, jsonify
from app.chat import AIThinkingAssistant
import asyncio
import json

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Initialize the AI assistant
ai_assistant = AIThinkingAssistant()


# Load course resources from resource.json
with open('resource.json', 'r') as f:
    resources = json.load(f)

@app.route("/", methods=["GET"])
def index():
    """Render the chatbot page."""
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    """
    Process user queries, returning course links if applicable,
    or delegating the query to the AI assistant otherwise.
    """
    try:
        # Extract the query from the request
        data = request.json
        query = data.get("query", "").strip().lower()

        if not query:
            return jsonify({"response": "Invalid input. Please type a query."}), 400

        # Match the query against course resources
        for course_key, link in resources.items():
            if course_key.replace('_', ' ') in query:  # Check for a match
                course_name = course_key.replace('_', ' ').title()
                return jsonify({"response": f"The link for {course_name} is: {link}"})

        # If no course match, use the AI assistant
        response = asyncio.run(ai_assistant.generate_response(query))
        return jsonify({"response": response})

    except Exception as e:
        # Log and return error message
        print(f"Error occurred: {str(e)}")
        return jsonify({"response": f"An error occurred: {str(e)}"}), 500
