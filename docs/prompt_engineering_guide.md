# 🧠 The Golden Rules & Principles of Prompt Engineering

Prompt Engineering is the art and science of communicating effectively with Large Language Models (LLMs). Writing a prompt is not like searching Google with keywords; it is like delegating a task to a smart, capable assistant who has no context about your specific business unless you provide it.

Below are the **Golden Rules and Core Principles of Prompt Engineering** that will help you design enterprise-ready prompts for any application.

---

## 🏆 The 10 Golden Rules of Prompt Engineering

### Rule 1: Assign a Clear Role (Persona)
LLMs are trained on vast amounts of diverse text. Giving the AI a specific persona helps it narrow down its vocabulary, tone, and domain expertise.

*   **❌ Bad:** `Summarize this order details: [data]`
*   **✅ Good:** `You are an expert Oracle Siebel CRM Analyst. Your task is to analyze order details and summarize them into a concise, professional business update for account managers. Use clear bullet points and highlight any potential risks.`

---

### Rule 2: Provide Detailed Context
An LLM cannot guess your background or goals. Explain *why* you are asking and *who* will read the output.

*   **❌ Bad:** `Draft an email about the server delay.`
*   **✅ Good:** `Draft a formal email to our client, Acme Corp. Explain that our UAT integration environment is experiencing a 4-hour delay due to Siebel database maintenance. Apologize for the inconvenience and assure them that our team is monitoring it.`

---

### Rule 3: Use Clear Delimiters to Separate Instruction from Input Data
Use delimiters like triple quotes `"""`, triple backticks ` ``` `, XML tags `<data></data>`, or headers to help the model distinguish where your instructions end and the input data begins. This prevents "prompt injection" (where the data tricks the model).

*   **❌ Bad:** `Summarize the following text. Acme Corp is renewing their contract...`
*   **✅ Good:**
    ```text
    Summarize the text enclosed in triple backticks into 3 bullet points.
    
    ```
    Acme Corp is renewing their contract. They requested a 10% discount on support licenses.
    ```
    ```

---

### Rule 4: Specify the Desired Output Format (Structure)
Tell the AI exactly how you want the response structured. You can ask for Bullet Points, Markdown, JSON, HTML, or CSV.

*   **❌ Bad:** `Give me a list of products from this notes field.`
*   **✅ Good:**
    ```text
    Extract all product names and their quantities mentioned in the notes. 
    Return the result strictly as a valid JSON array of objects with the keys "product_name" and "quantity".
    Example output format:
    [
      {"product_name": "CRM License", "quantity": 10}
    ]
    ```

---

### Rule 5: Show, Don't Just Tell (Few-Shot Prompting)
Giving the model one or two examples of the desired input and output pattern (known as "Few-Shot Prompting") dramatically improves its accuracy and consistency.

*   **❌ Bad:** `Convert these dates to YYYY-MM-DD format.`
*   **✅ Good:**
    ```text
    Convert the following dates into the standard format (YYYY-MM-DD).
    
    Input: Jan 15th, 2026
    Output: 2026-01-15
    
    Input: 12/05/2025
    Output: 2025-12-05
    
    Input: October 8, 2024
    Output: 2024-10-08
    
    Input: [Your date here]
    Output:
    ```

---

### Rule 6: Chain of Thought (Ask the AI to "Think Step-by-Step")
For complex logic, reasoning, or math, tell the AI to think or explain its reasoning before outputting the final answer. This forces the model to trace logical steps instead of rushing to a guess.

*   **❌ Bad:** `Is SBL-ORD-102 a priority order? Support renewal date is 2026-09-30 and the current date is 2026-06-21. Today is less than 90 days before renewal.`
*   **✅ Good:** `Analyze whether the support renewal is critical (less than 90 days away). Think step-by-step. First calculate the number of days between the current date (2026-06-21) and the renewal date (2026-09-30), then decide if it falls under 90 days, and explain your conclusion.`

---

### Rule 7: Define Negative Constraints (What NOT to do)
Specify boundaries to keep the AI on track. Tell it what to avoid or what to do if it doesn't know the answer.

*   **❌ Bad:** `Summarize the order.`
*   **✅ Good:** `Summarize the order details. Do NOT include any technical IDs or database row keys. If any information is missing (like shipping address), write "Not Provided" instead of making up a value.`

---

### Rule 8: Control Creativity (Adjusting Temperature)
Temperature is a setting (0.0 to 1.0) that controls the model's randomness:
*   **Low Temperature (0.0 to 0.3):** Best for facts, data extraction, code generation, and standard summaries. (Used in our Siebel POC).
*   **High Temperature (0.7 to 1.0):** Best for creative writing, brainstorming, and marketing copy.

---

### Rule 9: Be Direct and Clear (Avoid Fluff)
LLMs process word tokens. Avoid saying "please", "would you mind", or adding conversational fluff. Clear, imperative sentences work best.

*   **❌ Bad:** `Hi! I was wondering if you could please be so kind as to read this text and give me a summary when you have a moment? Thank you!`
*   **✅ Good:** `Summarize the following text in 3 sentences.`

---

### Rule 10: Iterate, Test, and Refine
Prompt engineering is an experimental science. If the output isn't perfect:
1. Identify where it failed.
2. Update the prompt to add a rule or example addressing that specific failure.
3. Test again with multiple different inputs to ensure the change didn't break other cases.

---

## 💡 Summary Reference Card

| Principle | Description | Why it works |
| :--- | :--- | :--- |
| **Persona** | Assign a role (e.g., "Siebel Analyst") | Narrows the AI's domain focus |
| **Context** | Explain background and target audience | Tailors detail and tone |
| **Delimiters** | Use `"""` or XML tags | Prevents confusion between instructions and data |
| **Few-Shot** | Show 1-2 examples | Teaches pattern recognition |
| **Chain-of-Thought** | "Think step-by-step" | Improves logical reasoning |
| **Constraints** | State what *not* to do | Prevents AI hallucination and fluff |
| **Temperature** | Low for facts, High for creativity | Controls randomness |

---

## 🎨 Enterprise Examples (Siebel CRM Context)

Here is a comparison of how prompt engineering changes the output for a Siebel CRM integration:

### ⚠️ Level 1: Beginner Prompt (No engineering)
> "Summarize the order notes: Customer wants to add 5 licenses but is complaining about the CRM portal load speed."

**Potential Output:**
> The customer wants to buy 5 more CRM licenses. However, they are having issues with portal speed.

---

### 🚀 Level 2: Engineered Prompt (Enterprise Ready)
> You are a Senior Customer Success Manager. Analyze the following CRM customer interaction note.
> Provide a structured summary with the following three sections:
> 1. **Revenue Opportunity**: Identify upsell details.
> 2. **Technical Issues**: Identify any system pain points.
> 3. **Action Items**: Recommend next steps for the account manager.
> Keep the tone professional and action-oriented.
>
> Note: "Customer wants to add 5 licenses but is complaining about the CRM portal load speed."

**Output:**
> ### 1. Revenue Opportunity
> *   **License Upsell**: Customer has expressed intent to acquire 5 additional Siebel CRM licenses.
> 
> ### 2. Technical Issues
> *   **Performance degradation**: Customer is experiencing latency/load speed issues within the CRM portal.
> 
> ### 3. Action Items
> *   **Sales follow-up**: Account Manager should initiate the procurement process for the 5 new licenses.
> *   **Support escalation**: Log a technical support ticket to analyze portal performance and database query optimization.
