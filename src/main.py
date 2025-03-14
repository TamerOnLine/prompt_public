import logging
from ai_agent import initialize_ai_agent 
from database import setup_database, store_response
from utils import setup_logging, save_to_markdown
from config import DEFAULT_MODEL
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

def main():
    setup_logging()
    setup_database()
    

    model_name = input("Enter AI model name (default: mistral): ").strip() or DEFAULT_MODEL
    temperature = float(input("Enter temperature (default: 0.1): ").strip() or 0.1)


    agent = initialize_ai_agent(model_name)

    topic = input("Enter the topic of interest: ").strip()
    tools_list = agent.get_relevant_tools(topic)  # استدعاء الدالة من داخل الكائن

    if not tools_list:
        print("❌ No relevant tools found. Try another topic.")
        return

    print("\n🔹 Relevant tools/people/books for your topic:")
    for idx, tool in enumerate(tools_list, start=1):
        print(f"{idx}. {tool}")

    while True:
        try:
            choice = int(input("\nEnter the number of the tool/method you want to explore: ")) - 1
            if 0 <= choice < len(tools_list):
                tool = tools_list[choice]
                break
            else:
                print("❌ Invalid choice. Please choose a valid number.")
        except ValueError:
            print("❌ Please enter a valid number.")

    print("\nSelect preferred explanation style:")
    explanation_styles = ["Brief", "Detailed", "Step-by-step"]
    for idx, style in enumerate(explanation_styles, start=1):
        print(f"{idx}. {style}")

    while True:
        try:
            explanation_choice = int(input("Enter the number of preferred explanation style: ")) - 1
            if 0 <= explanation_choice < len(explanation_styles):
                explanation_style = explanation_styles[explanation_choice]
                break
            else:
                print("❌ Invalid choice. Please choose a valid number.")
        except ValueError:
            print("❌ Please enter a valid number.")

    print("\nChoose response accuracy level:")
    accuracy_levels = ["Low", "Medium", "High"]
    for idx, level in enumerate(accuracy_levels, start=1):
        print(f"{idx}. {level}")

    while True:
        try:
            accuracy_choice = int(input("Enter the number of accuracy level: ")) - 1
            if 0 <= accuracy_choice < len(accuracy_levels):
                accuracy_level = accuracy_levels[accuracy_choice]
                break
            else:
                print("❌ Invalid choice. Please choose a valid number.")
        except ValueError:
            print("❌ Please enter a valid number.")

    print(f"\n🔍 Exploring {tool} in relation to {topic}...")

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"You are an AI assistant. The user is interested in {topic} using {tool}. "
                   f"Provide a {explanation_style.lower()} explanation with {accuracy_level.lower()} accuracy.")
    ])

    response_text = agent.generate_response(topic, tool)

    if response_text:
        reference_link = store_response(topic, tool, response_text)
        save_to_markdown(topic, tool, response_text, reference_link)

        print("\n📚 AI Response:")
        print("=" * 50)
        print(response_text)
        print("=" * 50)
        print(f"🔗 Reference: {reference_link}")
        print("✅ Response saved in database and a unique Markdown file in 'save_md/'.")
    else:
        print("❌ Failed to generate AI response.")

if __name__ == "__main__":
    main()
