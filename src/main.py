import os
import re
import time
import logging
import sqlite3
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
import webbrowser

def setup_logging():
    """Configure logging with detailed error messages."""
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def setup_database():
    """Initialize the SQLite database to store responses."""
    conn = sqlite3.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            tool TEXT,
            explanation_style TEXT,
            accuracy_level TEXT,
            response_text TEXT,
            reference_link TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_reference_link(topic, tool):
    """Generate a dynamic reference link based on the topic and tool."""
    base_url = "https://www.google.com/search?q="
    query = f"{topic}+{tool}+tutorial"
    return base_url + query.replace(" ", "+")

def store_response(topic, tool, explanation_style, accuracy_level, response_text):
    """Store AI responses in SQLite database with a reference link."""
    reference_link = generate_reference_link(topic, tool)
    conn = sqlite3.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO responses (topic, tool, explanation_style, accuracy_level, response_text, reference_link)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (topic, tool, explanation_style, accuracy_level, response_text, reference_link))
    conn.commit()
    conn.close()
    return reference_link

def get_past_responses():
    """Retrieve past responses from the database."""
    conn = sqlite3.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, topic, tool, response_text, reference_link, timestamp FROM responses ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return records

def generate_response(llm, prompt):
    """Generate AI response."""
    try:
        response = llm.invoke(prompt)
        return response.content.strip() if hasattr(response, "content") else None
    except Exception as error:
        logging.error("Error while generating response: %s", str(error))
        return None

def main():
    """Main function to run the assistant."""
    setup_logging()
    setup_database()
    
    model_name = input("Enter AI model name (default: mistral): ").strip() or "mistral"
    llm = ChatOllama(model=model_name, temperature=0.9)
    
    topic = input("Enter the topic of interest: ").strip()
    tool = input("Enter the tool/method: ").strip()
    explanation_style = input("Preferred explanation style ('brief', 'detailed', 'step-by-step')? ").strip().lower()
    accuracy_level = input("Choose response accuracy level ('Low', 'Medium', 'High'): ").strip().capitalize()
    
    if accuracy_level not in ["Low", "Medium", "High"]:
        logging.warning("Invalid accuracy level entered. Defaulting to 'Medium'.")
        accuracy_level = "Medium"
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"You are an AI assistant. The user is interested in {topic} using {tool}. Prefers {explanation_style} explanation. Accuracy: {accuracy_level}.")
    ])
    
    prompt_filled = prompt_template.format(
        topic=topic, tool=tool, explanation_style=explanation_style, accuracy_level=accuracy_level
    )
    
    response_text = generate_response(llm, prompt_filled)
    
    if response_text:
        reference_link = store_response(topic, tool, explanation_style, accuracy_level, response_text)
        print("\n📚 AI Response:")
        print("=" * 50)
        print(response_text)
        print("=" * 50)
        print(f"🔗 Reference: {reference_link}")
        print("✅ Response saved in database.")
    else:
        print("❌ Failed to generate AI response.")
    
    # Fetch past responses
    past_responses = get_past_responses()
    print("\n📜 Past Responses:")
    for rec in past_responses[:5]:  # Show last 5 responses
        print(f"[{rec[0]}] {rec[1]} using {rec[2]} - {rec[5]}\n{rec[3][:200]}...")  # Truncate response for display
        print(f"🔗 Reference: {rec[4]}")
        print("-" * 50)

if __name__ == "__main__":
    main()
