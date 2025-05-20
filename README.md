# 🍔 BITE – Bot for Interactive Tasty Engagement 🤖

<div align="center">
  
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Dialogflow](https://img.shields.io/badge/Dialogflow-FF9800?style=for-the-badge&logo=dialogflow&logoColor=white)](https://cloud.google.com/dialogflow)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)

</div>

A smart food ordering assistant that provides seamless conversational ordering experience through website integration.

## 🌟 Key Features

- 🗣️ **Natural Language Processing** - Powered by Dialogflow for human-like interactions
- 🚀 **FastAPI Backend** - High-performance Python backend for order processing
- 🛒 **Smart Cart Management** - Session-based cart with order tracking
- 📊 **MySQL Database** - Reliable data storage for orders and user interactions
- 🌐 **Web Integration** - Easy-to-use chatbot widget for any website

## 📦 Project Structure

```
BITE-Bot/
│
├── src/              # FastAPI backend (handles requests from Dialogflow)
│   ├── main.py           # Main FastAPI application
│   ├── db_helper.py      # Database helper functions
│   ├── utils.py          # Utility functions
│   └── requirements.txt  # Python dependencies
│
├── frontend/             # Website source code
│   ├── home.html         # Main HTML page
│   ├── styles.css        # CSS styles
│   ├── banner.jpg        # Banner image
│   ├── menu1.jpg         # Menu images
│   ├── menu2.jpg
│   └── menu3.jpg
│
├── db/                   # MySQL database dump (import via Workbench)
│   └── eatery.sql
│
└── dialogflow_assets/    # Dialogflow intents, training phrases, and configurations
    └── training_phrases.txt
```

## 🚀 Quick Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- ngrok account (for local testing)
- Google Cloud account (for Dialogflow)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dinesh5aini/BITE-Bot.git
   cd BITE-Bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r src/requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install mysql-connector
   pip install "fastapi[all]"
   ```

3. **Database setup**
   - Import `db/eatery.sql` into MySQL Workbench

4. **Start the FastAPI backend**
   ```bash
   cd src
   uvicorn main:app --reload
   ```

5. **Set up ngrok for HTTPS tunneling**
   - Download ngrok from https://ngrok.com/download
   - Extract the zip file and place ngrok.exe in a folder
   - Open command prompt, navigate to that folder and run:
   ```bash
   ngrok http 8000
   ```
   - **Note**: ngrok sessions can timeout. You'll need to restart the session if you see a "session expired" message.

6. **Dialogflow integration**
   - Create a new agent in Dialogflow Console
   - Import intents from dialogflow_assets folder
   - Set fulfillment webhook URL to your ngrok HTTPS URL

7. **Access the website**
   - Open `frontend/home.html` in your browser to see the chatbot in action

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  Built as a learning project ✨<br>
  <a href="https://github.com/Dinesh5aini/BITE-Bot">GitHub</a>
</div>