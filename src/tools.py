import os
import re
import sqlite3
import requests
from googlesearch import search
from bs4 import BeautifulSoup
from datetime import datetime
from langchain_core.tools import Tool

# ✅ توليد رابط بحث في Google
def generate_reference_link(topic, tool):
    """Generate a Google search link as a reference."""
    base_url = "https://www.google.com/search?q="
    query = f"{topic} {tool} tutorial"
    return base_url + query.replace(" ", "+")

generate_reference_link_tool = Tool(
    name="generate_reference_link",
    func=generate_reference_link,
    description="Generate a Google search link based on the topic and tool.",
    return_direct=True,
)

# ✅ البحث عبر Google (يتطلب Scraper API للاستخدام الفعلي)


def google_search(query: str, num_results=5) -> list:
    """Perform a Google search using `googlesearch` package."""
    try:
        results = list(search(query, num=num_results, stop=num_results, pause=2))
        return results
    except Exception as e:
        return [f"❌ Error: {e}"]


search_googlesearch_tool = Tool(
    name="search_googlesearch",
    func=google_search,
    description="Perform a Google search and return top results.",
    return_direct=True,
)

# ✅ تنظيف أسماء الملفات
def sanitize_filename(name):
    """Remove invalid characters from filenames."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)

sanitize_filename_tool = Tool(
    name="sanitize_filename",
    func=sanitize_filename,
    description="Sanitize file names by removing invalid characters.",
    return_direct=True,
)

# ✅ تخزين الاستجابات في قاعدة البيانات
def store_response(topic, tool, response_text):
    """Store the AI-generated response in the SQLite database."""
    reference_link = generate_reference_link(topic, tool)
    conn = sqlite3.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO responses (topic, tool, response_text, reference_link)
        VALUES (?, ?, ?, ?)
    ''', (topic, tool, response_text, reference_link))
    conn.commit()
    conn.close()
    return reference_link

store_response_tool = Tool(
    name="store_response",
    func=store_response,
    description="Store AI-generated response in the database.",
    return_direct=True,
)

# ✅ حفظ الاستجابة في ملف Markdown
def save_to_markdown(topic, tool, response_text, reference_link):
    """Save AI-generated response as a Markdown file."""
    save_path = os.path.join("save_md")
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_topic = sanitize_filename(topic)
    sanitized_tool = sanitize_filename(tool)
    filename = f"{sanitized_topic}_{sanitized_tool}_{timestamp}.md"
    file_path = os.path.join(save_path, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {topic} - {tool}\n")
        f.write(f"**Response:**\n\n{response_text}\n")
        f.write(f"🔗 **Reference:** [{reference_link}]({reference_link})\n")

    return file_path

save_to_markdown_tool = Tool(
    name="save_to_markdown",
    func=save_to_markdown,
    description="Save AI response as a Markdown file.",
    return_direct=True,
)

# ✅ استخراج محتوى من مواقع الإنترنت
def scrape_website(url: str) -> str:
    """Scrape content from a given URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
        return "❌ Failed to scrape website."
    except Exception as e:
        return f"❌ Error: {e}"

scrape_website_tool = Tool(
    name="scrape_website",
    func=scrape_website,
    description="Scrape content from a given website.",
    return_direct=True,
)

# ✅ تحميل واستعلام FAISS (غير مستخدم حالياً، ولكن محفوظ)
def load_faiss():
    """Placeholder for loading FAISS index."""
    pass

load_faiss_tool = Tool(
    name="load_faiss",
    func=load_faiss,
    description="Load FAISS index (currently a placeholder).",
    return_direct=True,
)

def search_faiss():
    """Placeholder for searching in FAISS index."""
    pass

search_faiss_tool = Tool(
    name="search_faiss",
    func=search_faiss,
    description="Search in FAISS index (currently a placeholder).",
    return_direct=True,
)

# ✅ التقاط استجابة المستخدم (للتفاعل)
def user_response(input_text):
    """Simulate a user response for debugging purposes."""
    return f"User said: {input_text}"

user_response_tool = Tool(
    name="user_response",
    func=user_response,
    description="Simulate user response.",
    return_direct=True,
)

# ✅ أداة إدخال استفسارات (Placeholder)
def input_query():
    """Placeholder function for user query input."""
    pass

input_query_tool = Tool(
    name="input_query",
    func=input_query,
    description="Placeholder for user query input.",
    return_direct=True,
)

# ✅ جميع الأدوات المجموعة
tools = [
    generate_reference_link_tool,
    search_googlesearch_tool,
    sanitize_filename_tool,
    store_response_tool,
    save_to_markdown_tool,
    scrape_website_tool,
    load_faiss_tool,
    search_faiss_tool,
    user_response_tool,
    input_query_tool
]
