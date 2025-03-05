# **📌Project Overview**
The **Chat AI** project is a Django-based application that allows users to interact with a **LLM (Large Language Model)** of their choice using the **Ollama** library.  
It provides a simple and efficient interface to communicate with an AI model configured according to the user's preference.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## **✨Features**
- ### **Chat with an LLM**: 
  - Users can ask questions and receive responses from a selected language model.
- ### **Model Customization**: 
  - Users can specify the AI model they want to use via the **AI_MODEL** variable in `settings.py`.
- ### **Bootstrap Frontend**: 
  - Integrated **Bootstrap** for a clean and responsive UI.
- ### **HTMX Integration**: 
  - Enhanced user experience with **HTMX**, enabling dynamic interactions without page reloads.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## **⚙️Installation Guide**

### **Prerequisites**
- Install **Ollama**: [https://ollama.com/](https://ollama.com/)
- Download a **LLM** of your choice compatible with Ollama.

### **Django Project Installation**

1. **Clone the Repository**:
   ```
   git clone https://github.com/sundayz-hunter/Chat_AI
   ```
   
2. **Create and Activate a Virtual Environment**:
   - On **Windows**:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Environment File**: 
   - Rename `.env-dist` to `.env` without modifications to use the default SQLite3 setup, or adjust it based on your database.
   

5. **AI Model Configuration**:
   - Open `settings.py` and modify the **AI_MODEL** variable to specify the desired language model:
     ```
     AI_MODEL = "your_model_name"
     ```

6. **Database Setup**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Start the Server**:
   ```
   python manage.py runserver
   ```

8. **Use the Application**:
   - Once the server is running, visit **http://127.0.0.1:8000**, create an account and start chatting with the AI.
