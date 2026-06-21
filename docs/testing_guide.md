# 🧪 Testing Guide — Oracle Siebel × Gen AI POC

## Quick Start

Both servers are running. Open your browser and go to:

### 👉 **http://localhost:8000**

This will open the **Order Summarization Dashboard** — a beautiful UI where you can:
1. Enter order details (pre-filled with sample data)
2. Optionally ask a specific question about the order
3. Click **"✨ Generate AI Summary"** to get an AI-powered response

---

## Testing Methods

### 1. 🖥️ Web UI (Recommended)
- Open **http://localhost:8000** in your browser
- The form is pre-filled with sample Siebel order data
- Click "Generate AI Summary" to test immediately
- Try typing questions like:
  - *"What upsell opportunities exist for this customer?"*
  - *"What are the risks in this order?"*
  - *"Summarize this for a management review"*

### 2. 📘 Swagger UI (Interactive API Docs)
- Open **http://localhost:8000/docs**
- Click on `POST /api/v1/summarize-order`
- Click "Try it out"
- Paste the sample JSON (below) and click "Execute"

### 3. 🔧 PowerShell / Command Line
```powershell
$body = @{
    order_id = "SBL-ORD-2026-0847"
    customer_name = "Acme Corporation"
    order_date = "2026-06-20"
    status = "In Progress"
    priority = "High"
    line_items = @(
        @{
            product_name = "Enterprise CRM License"
            quantity = 10
            unit_price = 1200.00
            total_price = 12000.00
        },
        @{
            product_name = "Premium Support Package"
            quantity = 1
            unit_price = 5000.00
            total_price = 5000.00
        }
    )
    total_amount = 17000.00
    currency = "USD"
    notes = "Key account"
    user_question = "What risks do you see in this order?"
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/summarize-order" `
    -Method Post -Body $body -ContentType "application/json" -TimeoutSec 300
```

### 4. 🧰 Postman / cURL
```bash
curl -X POST http://localhost:8000/api/v1/summarize-order \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "SBL-ORD-2026-0847",
    "customer_name": "Acme Corporation",
    "order_date": "2026-06-20",
    "status": "In Progress",
    "line_items": [{"product_name": "CRM License", "quantity": 5, "unit_price": 1200, "total_price": 6000}],
    "total_amount": 6000,
    "user_question": "Summarize this order for management review"
  }'
```

---

## Simulating Oracle Siebel Integration

For your POC demo, here's how Siebel would integrate with this API:

### Option A: Siebel Workflow → REST API Call
1. Create a **Siebel Workflow** triggered on Order creation/update
2. Use the **EAI HTTP Transport** business service to call:
   - URL: `http://<your-server>:8000/api/v1/summarize-order`
   - Method: POST
   - Content-Type: application/json
3. Map Siebel order fields to the JSON payload
4. Store the AI summary back in a Siebel field

### Option B: Siebel Open UI Script
1. Add a button "Get AI Summary" on the Order Form Applet
2. Use `XMLHttpRequest` or `fetch()` in a PR script to call the API
3. Display the summary in a popup or text field

### Option C: Middleware (Oracle Integration Cloud / MuleSoft)
1. Set up an integration flow that reads Siebel orders
2. Calls this API for summarization
3. Writes the summary back to Siebel

---

## API Endpoints Reference

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Opens the Web UI Dashboard |
| GET | `/health` | Health check (provider + model info) |
| GET | `/docs` | Swagger UI (interactive API testing) |
| GET | `/redoc` | ReDoc API documentation |
| POST | `/api/v1/summarize-order` | Generate AI summary for an order |

---

## Restarting the Servers

If the servers stop, restart them with:

```powershell
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start FastAPI
cd "c:\Users\Admin\Documents\GEN AI POC"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Notes
- ⏱️ **Response time**: ~1-2 minutes on CPU (no GPU). Switch to OpenAI/Claude for instant responses.
- 🔄 **Switch providers**: Edit `.env` → change `LLM_PROVIDER` to `openai` or `anthropic` and add your API key.
- 🔐 **Security**: CORS is wide-open for POC. Lock it down before production.
