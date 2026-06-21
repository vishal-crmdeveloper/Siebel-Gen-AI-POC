# 🎓 Complete Visual Learning Guide
## From Zero to Confident — Understanding Every Line of Your POC

> [!TIP]
> Read this top-to-bottom, like a story. By the end, you will understand every single thing happening behind the scenes.

---

## 📁 Your Project Structure (The Big Picture)

```
GEN AI POC/
│
├── .env                    ← ⚙️ Settings file (which AI to use, passwords)
│
├── app/                    ← 🧠 The "brain" folder (all backend logic)
│   ├── config.py           ← Reads settings from .env
│   ├── models.py           ← Defines the shape of data (what fields are expected)
│   ├── llm_service.py      ← Builds the prompt + talks to the AI
│   └── main.py             ← The "front door" — receives HTTP requests
│
├── static/
│   └── index.html          ← 🎨 The premium web UI
│
├── streamlit_app.py        ← 🎨 The Streamlit UI (alternative)
└── start_servers.bat       ← 🚀 One-click launcher
```

Think of it as a **company**:
- `main.py` = **The Receptionist** (receives visitors/requests)
- `models.py` = **The Form Template** (what information to collect)
- `llm_service.py` = **The Expert** (builds the question and talks to AI)
- `config.py` = **The Settings Panel** (which AI provider to use)

---

## 📄 File 1: `.env` — The Settings File

This is the simplest file. It's like a control panel with switches.

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

**In plain English:**
| Line | What it means |
|------|---------------|
| `LLM_PROVIDER=ollama` | "Use Ollama as our AI engine" |
| `OLLAMA_BASE_URL=http://localhost:11434` | "Ollama is running on this same computer, on apartment 11434" |
| `OLLAMA_MODEL=llama3.2` | "Use the LLaMA 3.2 brain" |

> [!IMPORTANT]
> **Interview Question:** *"Can you switch AI providers?"*
> **Your Answer:** "Yes. I change one line: `LLM_PROVIDER=openai` and add `OPENAI_API_KEY=sk-xxxxx`. Zero code changes needed. The architecture uses a Strategy Pattern."

---

## 📄 File 2: `config.py` — Reading the Settings

This file reads the `.env` file and makes those settings available to the rest of the code.

```python
import os                          # ← Python's tool to read system settings
from dotenv import load_dotenv     # ← Tool that reads the .env file

load_dotenv()                      # ← "Hey Python, please read my .env file now"

class Settings:
    # Read each setting. If not found, use the default value after the comma.
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    #              ↑                    ↑               ↑
    #         data type          setting name      default value

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

settings = Settings()  # ← Create one global "settings" object everyone can use
```

**What this does:** Imagine a secretary who reads a paper form (`.env`) at the start of the day and remembers all the answers. Any department can ask the secretary: *"Hey, what's our AI provider?"* and she says *"Ollama."*

---

## 📄 File 3: `models.py` — The Data Blueprint

This file defines **exactly what shape** the incoming data must be. Think of it as a **form template** — if someone fills it out wrong, it gets rejected before the AI even sees it.

### Part A: What does ONE line item look like?

```python
class OrderLineItem(BaseModel):
    product_name: str          # ← Must be text.     Example: "CRM License"
    quantity: int              # ← Must be a number.  Example: 10
    unit_price: float          # ← Must be a decimal. Example: 1200.00
    total_price: float         # ← Must be a decimal. Example: 12000.00
    product_id: Optional[str]  # ← Optional text.     Can be empty/null
    discount: Optional[float]  # ← Optional decimal.  Can be empty/null
```

**Visual example — one line item as JSON:**
```json
{
    "product_name": "Enterprise CRM License",
    "quantity": 10,
    "unit_price": 1200.00,
    "total_price": 12000.00
}
```

### Part B: What does the FULL order request look like?

```python
class OrderSummaryRequest(BaseModel):
    order_id: str              # ← REQUIRED. Example: "SBL-ORD-2026-0847"
    customer_name: str         # ← REQUIRED. Example: "Acme Corporation"
    order_date: str            # ← REQUIRED. Example: "2026-06-20"
    status: str                # ← REQUIRED. Example: "In Progress"
    line_items: list[...]      # ← REQUIRED. At least 1 item
    total_amount: float        # ← REQUIRED. Example: 20000.00
    currency: str              # ← Has default "USD"
    notes: Optional[str]       # ← OPTIONAL. Can be null
    priority: Optional[str]    # ← OPTIONAL. Can be null
    shipping_address: Optional[str]  # ← OPTIONAL
    user_question: Optional[str]     # ← OPTIONAL. Your question to the AI
```

### 🔥 The ACTUAL JSON that gets sent from the UI to FastAPI:

```json
{
    "order_id": "SBL-ORD-2026-0847",
    "customer_name": "Acme Corporation",
    "order_date": "2026-06-20",
    "status": "In Progress",
    "priority": "High",
    "line_items": [
        {
            "product_name": "Enterprise CRM License",
            "quantity": 10,
            "unit_price": 1200.00,
            "total_price": 12000.00
        },
        {
            "product_name": "Premium Support Package",
            "quantity": 1,
            "unit_price": 5000.00,
            "total_price": 5000.00
        },
        {
            "product_name": "Data Migration Service",
            "quantity": 1,
            "unit_price": 3000.00,
            "total_price": 3000.00
        }
    ],
    "total_amount": 20000.00,
    "currency": "USD",
    "notes": "Key account - customer requested expedited processing. Q3 renewal coming up.",
    "shipping_address": "123 Business Ave, Suite 500, New York, NY 10001",
    "user_question": "What risks do you see in this order?"
}
```

### Part C: What does the RESPONSE look like?

```python
class OrderSummaryResponse(BaseModel):
    order_id: str    # ← Same order ID echoed back
    summary: str     # ← The AI's answer (markdown text)
    provider: str    # ← "ollama"
    model: str       # ← "llama3.2"
```

### 🔥 The ACTUAL JSON that comes BACK from FastAPI to the UI:

```json
{
    "order_id": "SBL-ORD-2026-0847",
    "summary": "**Order Summary**\n\nThis is a high-priority order from Acme Corporation worth $20,000...",
    "provider": "ollama",
    "model": "llama3.2"
}
```

> [!IMPORTANT]
> **Interview Question:** *"What is Pydantic?"*
> **Your Answer:** "Pydantic is a Python validation library. It acts as a security guard — before any data reaches the AI, Pydantic checks every field (is it the right type? Is it within range? Is it missing?). If anything is wrong, it rejects the request with a 422 error. The AI never sees bad data."

---

## 📄 File 4: `llm_service.py` — The Heart of the System

This is the most important file. It does TWO things:
1. **Builds the prompt** (converts your form data into English sentences the AI can read)
2. **Calls the AI** (sends the prompt to Ollama/OpenAI/Anthropic)

### Part A: The Prompt Builder — `_build_prompt()`

This function takes the structured JSON data and converts it into a **natural language instruction** for the AI.

```python
def _build_prompt(order):

    # Step 1: Format each line item into a readable string
    items_text = ""
    for item in order.line_items:
        items_text += f"  - {item.product_name}: Qty {item.quantity} × ${item.unit_price} = ${item.total_price}\n"

    # Step 2: Check if user asked a specific question
    if order.user_question:
        instruction = f"""You are an AI assistant integrated with Oracle Siebel CRM.
A user has asked the following question about an order:

USER QUESTION: {order.user_question}

Analyze the order details below and provide a clear, professional answer."""
    else:
        instruction = """You are an AI assistant integrated with Oracle Siebel CRM.
Analyze the following order and provide a concise, professional summary."""

    # Step 3: Combine instruction + order data into one big prompt
    prompt = f"""{instruction}

ORDER DETAILS:
───────────────────────────────
Order ID      : {order.order_id}
Customer      : {order.customer_name}
Order Date    : {order.order_date}
Status        : {order.status}
Priority      : {order.priority}
Total Amount  : ${order.total_amount}

Line Items:
{items_text}

Notes         : {order.notes}
Shipping Addr : {order.shipping_address}
───────────────────────────────

Provide your response in a clear, professional format."""

    return prompt
```

### 🔥 The ACTUAL PROMPT that gets sent to the AI:

When you fill the form and ask *"What risks do you see?"*, this is the **exact text** that gets sent to the LLaMA brain:

```
You are an AI assistant integrated with Oracle Siebel CRM.
A user has asked the following question about an order:

USER QUESTION: What risks do you see in this order?

Analyze the order details below and provide a clear, professional answer.

ORDER DETAILS:
───────────────────────────────
Order ID      : SBL-ORD-2026-0847
Customer      : Acme Corporation
Order Date    : 2026-06-20
Status        : In Progress
Priority      : High
Currency      : USD
Total Amount  : $20,000.00

Line Items:
  - Enterprise CRM License: Qty 10 × $1,200.00 = $12,000.00
  - Premium Support Package: Qty 1 × $5,000.00 = $5,000.00
  - Data Migration Service: Qty 1 × $3,000.00 = $3,000.00

Notes         : Key account - customer requested expedited processing. Q3 renewal coming up.
Shipping Addr : 123 Business Ave, Suite 500, New York, NY 10001
───────────────────────────────

Provide your response in a clear, professional format.
```

> [!TIP]
> **This is "Prompt Engineering"** — the art of writing instructions for the AI. Notice how we structured it clearly with labels. The better the prompt, the better the AI's answer.

### Part B: Calling the AI — `_call_ollama()`

Once the prompt is built, this function sends it to Ollama:

```python
async def _call_ollama(prompt):
    model = "llama3.2"                                    # Which AI brain to use
    url = "http://localhost:11434/api/generate"            # Ollama's address

    # Send a POST request (like submitting a form on a website)
    response = await client.post(
        url,
        json={
            "model": "llama3.2",      # ← "Use this brain"
            "prompt": prompt,          # ← "Here's my question" (the big text above)
            "stream": False,           # ← "Give me the full answer at once, don't send word by word"
        },
    )

    data = response.json()            # ← Read the response
    return data["response"]           # ← Extract just the AI's answer text
```

### 🔥 The ACTUAL JSON sent to Ollama:

```json
{
    "model": "llama3.2",
    "prompt": "You are an AI assistant integrated with Oracle Siebel CRM.\nA user has asked the following question...\n\nORDER DETAILS:\n───────────────────────────────\nOrder ID: SBL-ORD-2026-0847\n...",
    "stream": false
}
```

### 🔥 The ACTUAL JSON that Ollama returns:

```json
{
    "model": "llama3.2",
    "response": "**Risk Analysis for Order SBL-ORD-2026-0847**\n\nBased on my analysis, here are the key risks:\n\n1. **High Value Order ($20,000)** - This is a significant order that requires careful handling...\n2. **Expedited Processing Request** - The customer has requested faster processing which may strain resources...\n3. **Q3 Renewal Dependency** - The notes mention an upcoming Q3 renewal...",
    "done": true,
    "total_duration": 52250290000
}
```

### Part C: The Strategy Pattern — How Provider Switching Works

```python
# This is like a phone directory
_PROVIDERS = {
    "ollama": _call_ollama,       # ← If provider = "ollama", call this function
    "openai": _call_openai,       # ← If provider = "openai", call this function
    "anthropic": _call_anthropic, # ← If provider = "anthropic", call this function
}

async def summarize_order(order):
    provider = settings.LLM_PROVIDER    # ← Read from .env: "ollama"
    prompt = _build_prompt(order)       # ← Build the English prompt
    call_fn = _PROVIDERS[provider]      # ← Look up: "ollama" → _call_ollama function
    response_text, model = await call_fn(prompt)  # ← Call it!
    return response_text, provider, model
```

**Visual explanation:**
```
.env says LLM_PROVIDER = "ollama"
          ↓
Code looks up "ollama" in the phone directory
          ↓
Finds: _call_ollama function
          ↓
Calls that function with the prompt
          ↓
Gets the AI response back
```

> [!IMPORTANT]
> **Interview Question:** *"What design pattern did you use for provider switching?"*
> **Your Answer:** "The Strategy Pattern. We have a dictionary that maps provider names to their respective functions. The code never uses if/else to check the provider — it simply looks up the function by name. This makes adding a new provider (like OCI) as simple as adding one new entry to the dictionary."

---

## 📄 File 5: `main.py` — The Front Door

This file is the **receptionist** of your application. It receives incoming HTTP requests and routes them to the right department.

```python
# Create the application
app = FastAPI(
    title="Siebel Order Summarization API",
    version="1.0.0",
)

# CORS = "Allow anyone to call this API" (for the browser UI)
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

### Route 1: The Home Page
```python
@app.get("/")                         # ← When someone visits localhost:8000
async def root():
    return RedirectResponse("/static/index.html")  # ← Show them the UI
```

### Route 2: Health Check
```python
@app.get("/health")                   # ← When someone visits localhost:8000/health
async def health_check():
    return {
        "status": "healthy",
        "provider": "ollama",
        "model": "llama3.2"
    }
```

### Route 3: The Main API (where the magic happens)
```python
@app.post("/api/v1/summarize-order")  # ← When someone sends order data here
async def summarize_order_endpoint(order: OrderSummaryRequest):
    #                                        ↑
    #                          Pydantic validates the JSON automatically!

    try:
        # Call the LLM service (builds prompt → calls AI → gets response)
        summary_text, provider, model = await summarize_order(order)

    except ValueError as exc:
        # If something is wrong with the data
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        # If the AI call itself failed
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}")

    # Return the successful response
    return {
        "order_id": order.order_id,
        "summary": summary_text,
        "provider": provider,
        "model": model,
    }
```

> [!IMPORTANT]
> **Interview Question:** *"What is FastAPI?"*
> **Your Answer:** "FastAPI is a modern Python web framework for building REST APIs. It automatically generates Swagger documentation at `/docs`, validates request data using Pydantic schemas, supports asynchronous processing for high performance, and provides built-in error handling. It's one of the fastest Python frameworks available."

---

## 🔄 The Complete Journey — Everything Together

Here is what happens when you click **"Generate AI Summary"**, shown as a **visual timeline**:

```
STEP 1: YOU CLICK THE BUTTON
┌─────────────────────────────────────────────────────────┐
│  Browser (index.html or Streamlit)                       │
│                                                          │
│  JavaScript collects all form fields                     │
│  Builds a JSON object                                    │
│  Sends: POST http://localhost:8000/api/v1/summarize-order│
│  Body: { "order_id": "SBL-...", "line_items": [...] }   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
STEP 2: FASTAPI RECEIVES IT
┌─────────────────────────────────────────────────────────┐
│  main.py → summarize_order_endpoint()                    │
│                                                          │
│  FastAPI reads the raw JSON bytes                        │
│  Pydantic checks: Is order_id a string? ✅              │
│  Pydantic checks: Is quantity ≥ 1? ✅                   │
│  Pydantic checks: At least 1 line item? ✅              │
│  Creates: OrderSummaryRequest Python object              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
STEP 3: PROMPT IS BUILT
┌─────────────────────────────────────────────────────────┐
│  llm_service.py → _build_prompt()                        │
│                                                          │
│  Takes structured data → converts to English text        │
│  Checks: Did user ask a question?                        │
│    YES → "Answer this question: What risks do you see?"  │
│    NO  → "Provide a general summary with 4 sections"     │
│  Output: A big text string (the "prompt")                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
STEP 4: AI IS CALLED
┌─────────────────────────────────────────────────────────┐
│  llm_service.py → _call_ollama()                         │
│                                                          │
│  Sends POST to http://localhost:11434/api/generate       │
│  Body: { "model": "llama3.2", "prompt": "...", ... }     │
│                                                          │
│  ⏳ WAITS 60-120 seconds (CPU inference)                 │
│                                                          │
│  Ollama tokenizes → 28 transformer layers → generates    │
│  Returns: { "response": "**Risk Analysis**\n..." }       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
STEP 5: RESPONSE SENT BACK
┌─────────────────────────────────────────────────────────┐
│  main.py wraps it in OrderSummaryResponse                │
│                                                          │
│  Returns JSON to browser:                                │
│  {                                                       │
│    "order_id": "SBL-ORD-2026-0847",                     │
│    "summary": "**Risk Analysis**\n\n1. High value...",   │
│    "provider": "ollama",                                 │
│    "model": "llama3.2"                                   │
│  }                                                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
STEP 6: UI DISPLAYS IT
┌─────────────────────────────────────────────────────────┐
│  Browser JavaScript                                      │
│                                                          │
│  Reads the JSON response                                 │
│  Converts **bold** → <strong>bold</strong>               │
│  Converts bullet points → <li> HTML elements             │
│  Shows provider badge: "ollama • llama3.2"               │
│  Shows response time: "⏱ 72.3s"                         │
│  Displays the beautiful formatted summary                │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Potential Interview Questions & Confident Answers

| Question | Your Answer |
|----------|-------------|
| *What framework did you use?* | "FastAPI — a high-performance Python REST framework with auto-generated Swagger docs and Pydantic validation." |
| *Why not Flask or Django?* | "FastAPI supports async natively, which is critical for LLM calls that take 60+ seconds. Flask would block the server during that time." |
| *How do you validate the data?* | "Pydantic schemas in models.py. Every field has a type, and required/optional status. Invalid data gets a 422 error before reaching the AI." |
| *What is the prompt?* | "A structured English instruction that tells the AI: who it is, what question to answer, and provides all the order data in a readable format." |
| *Can you switch AI providers?* | "Yes, by changing one environment variable. The Strategy Pattern in llm_service.py maps provider names to their respective HTTP call functions." |
| *Why is the response slow?* | "The POC runs LLaMA 3.2 (3 billion parameters) on CPU. In production, OCI Gen AI runs on NVIDIA A100 GPUs — response drops from 2 minutes to 3 seconds." |
| *Is the data secure?* | "In POC, everything runs on localhost — data never leaves the machine. In production, OCI VCN ensures all traffic stays within Oracle's private cloud." |
| *What is Ollama?* | "Ollama is an open-source tool that lets you run AI models locally on your own computer, like a private ChatGPT that doesn't need the internet." |
| *What is the difference between RAG and Prompt Engineering?* | "Prompt Engineering passes all data directly in the request. RAG adds a search step — it searches a knowledge base first, then includes the search results in the prompt. We use Prompt Engineering because order data is already available." |
| *Why not fine-tune the model?* | "Fine-tuning means retraining the model on thousands of examples. It's expensive and unnecessary for summarization — the base model already knows how to summarize text. We just need to give it good instructions (prompt engineering)." |
