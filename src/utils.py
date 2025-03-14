import logging
import re
import os

def setup_logging():
    """Setup logging for the application."""
    logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def sanitize_filename(name):
    """إزالة الأحرف غير الصالحة من أسماء الملفات"""
    return re.sub(r'[<>:"/\\|?*.,()]+', '_', name).strip()

def save_to_markdown(topic, tool, response_text, reference_link):
    """حفظ استجابة الذكاء الاصطناعي كملف Markdown بعد تنظيف الاسم"""
    save_path = os.path.join("save_md")
    os.makedirs(save_path, exist_ok=True)

    # 🔹 تنظيف اسم الملف لإزالة الأحرف غير الصالحة
    sanitized_topic = sanitize_filename(topic)
    sanitized_tool = sanitize_filename(tool)

    filename = f"{sanitized_topic}_{sanitized_tool}.md"
    file_path = os.path.join(save_path, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {topic} - {tool}\n")
            f.write(f"**Response:**\n\n{response_text}\n")
            f.write(f"🔗 **Reference:** [{reference_link}]({reference_link})\n")
        logging.info(f"Response saved to {file_path}")
    except OSError as e:
        logging.error(f"Failed to save file {file_path}: {e}")
        print(f"❌ Error saving file: {file_path}. Check filename validity.")
