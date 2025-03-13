Z# 🔍 FAISS Similarity Search Project

## 📌 Introduction
This project focuses on **similarity search using FAISS**, a powerful library by **Facebook AI** that enables fast search in high-dimensional data.

## ⚡ Features
- Supports **multiple data types** (text, images, audio, video, medical, geospatial, tabular, etc.).
- Uses **LangChain and Ollama** to generate AI-driven similarity search guides.
- Compatible with **multiple operating systems** with dedicated setup scripts.
- **GitHub Actions integration** for automated testing and validation.

---

## 📂 Project Structure

```bash
├── README.md  # This file
├── requirements.txt  # Dependencies
├── runtime.txt  # Python version required
├── src/  # Source code
│   ├── __init__.py
│   ├── main.py  # Main script for generating FAISS search guides using LangChain and Ollama
│   ├── runner.py  # Interactive script execution
├── tests/  # Unit tests
│   ├── __init__.py
│   ├── ollama.py  # Ollama test script
│   ├── test.py  # Main test runner
├── .github/workflows/  # CI/CD with GitHub Actions
│   ├── main.yml
├── Virtual Environment Setup
│   ├── activate_project.sh  (Linux & Mac)
│   ├── activate_project.bat  (Windows - CMD)
│   ├── activate_project.ps1  (Windows - PowerShell)

```
# FAISS Similarity Search Guides
---

### [🔍 Text Similarity Search](text_faiss_similarity_search.md)
### [📸 Image Similarity Search](images_faiss_similarity_search.md)
### [🎵 Audio Similarity Search](audio_faiss_similarity_search.md)
### [🎥 Video Similarity Search](video_faiss_similarity_search.md)
### [🏥 Medical Similarity Search](medical_faiss_similarity_search.md)
### [📊 Tabular Similarity Search](tabular_faiss_similarity_search.md)
### [🗺️ Geospatial Similarity Search](geospatial_faiss_similarity_search.md)
### [🤖 AI Embeddings Similarity Search](ai_embeddings_faiss_similarity_search.md)

## 🚀 How to Run

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Activate Virtual Environment
- **Linux & Mac:**
  ```bash
  source activate_project.sh
  ```
- **Windows (CMD):**
  ```cmd
  activate_project.bat
  ```
- **Windows (PowerShell):**
  ```powershell
  .\activate_project.ps1
  ```

### 3️⃣ Run the Project
```bash
python src/main.py
```

### 4️⃣ Run Tests
```bash
pytest tests/
```

---

## 🛠️ Technologies Used
- **FAISS** - Facebook AI Similarity Search
- **LangChain** - AI workflow management
- **Ollama** - Local AI query execution
- **Python 3.10+**
- **GitHub Actions** - CI/CD automation

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---

## 📞 Contact & Contributions
If you'd like to **contribute**, feel free to open a **Pull Request** or **create an Issue** on GitHub!

> **👨‍💻 Developer:** [TamerOnLine](https://github.com/TamerOnLine)

