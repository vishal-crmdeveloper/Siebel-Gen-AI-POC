# ⚡ Oracle Siebel × Gen AI POC

This is a Proof of Concept (POC) demonstrating how to integrate Oracle Siebel CRM with Generative AI (using Local LLaMA via Ollama). It features a robust FastAPI backend and a Streamlit dashboard.

---

## 🛠️ Prerequisites for Testing
To run this project on your machine, you will need:
1. **Python 3.10+**
2. **Ollama**: Download from [ollama.com](https://ollama.com/) and install it.

---

## 🚀 Setup Instructions

### Step 1: Download the Code
Clone this repository or download it as a ZIP file and extract it.
```bash
git clone https://github.com/vishal-crmdeveloper/Siebel-Gen-AI-POC.git
cd Siebel-Gen-AI-POC
```

### Step 2: Install Python Dependencies
Open your terminal inside the project folder and install the required packages:
```bash
pip install -r requirements.txt
```

### Step 3: Download the AI Model
Open a terminal and run this command to download the LLaMA 3.2 model (this may take a few minutes depending on your internet speed):
```bash
ollama pull llama3.2
```

---

## 🏃‍♂️ How to Run the App

You need to run two things at the same time: the Backend Server and the Frontend UI.

### Option A: The Easy Way (Windows Only)
Simply double-click the **`start_servers.bat`** file inside the folder. It will start both the Ollama engine and the FastAPI backend. Then open a new terminal and run:
```bash
python -m streamlit run streamlit_app.py
```

### Option B: Manual Start (Any OS)
**Terminal 1 (AI Engine):**
```bash
ollama serve
```

**Terminal 2 (Backend API):**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 3 (Frontend UI):**
```bash
python -m streamlit run streamlit_app.py
```

---

## 🧪 Testing the POC
1. Once the Streamlit app starts, your browser will open to `http://localhost:8501`.
2. The form will be pre-filled with sample Siebel Order data.
3. Type a question like *"What are the risks in this order?"*
4. Click **Generate AI Summary** and wait for the local model to process the request.
