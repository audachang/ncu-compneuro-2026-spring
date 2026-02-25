# Week 14: AI Features with the Claude API

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 14 of 16 | **Date:** 2026-05-28 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Install the Anthropic Python SDK and call `client.messages.create()`
2. Write effective system prompts that scope Claude's behaviour to your application
3. Stream a response token-by-token and display it in Streamlit
4. Build a conversational chat interface with `st.chat_message()` and `st.chat_input()`
5. Store API keys safely using `.env` locally and `st.secrets` on Streamlit Cloud
6. Identify the limits and risks of AI features and apply responsible design practices

---

## In-Class Topics

### 1. Installing the Anthropic SDK (5 min)

```bash
pip install anthropic python-dotenv
```

Add both to `requirements.txt`:
```
anthropic>=0.25
python-dotenv>=1.0
```

---

### 2. Your First API Call (20 min)

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")   # never hardcode keys — see Section 5

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=512,
    messages=[
        {"role": "user", "content": "What does an AQI value of 120 mean for health?"}
    ],
)

print(message.content[0].text)
```

The `messages` list follows a conversation format: alternate `user` and `assistant` turns. For a single question, provide one `user` message.

**Response object structure:**
```python
message.id             # unique message ID
message.model          # model used
message.usage          # input and output token counts
message.content[0].text  # the text of the response
message.stop_reason    # "end_turn", "max_tokens", etc.
```

---

### 3. System Prompts (20 min)

A system prompt sets the role, scope, and constraints for Claude's behaviour. A well-written system prompt keeps the AI feature focused and prevents off-topic responses.

```python
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=512,
    system=(
        "You are a public health assistant for a Taiwan air quality dashboard. "
        "Your role is to explain air quality index values and their health implications "
        "in clear, non-technical language suitable for the general public. "
        "Keep responses under 150 words. "
        "If asked about topics unrelated to air quality or public health, politely decline."
    ),
    messages=[
        {"role": "user", "content": "The AQI today is 145. Should I go jogging?"}
    ],
)
```

**System prompt design principles:**
- State the role explicitly ("You are a...")
- Define what is in scope and what is out of scope
- Set response length constraints
- Specify the audience (expert vs. general public)
- Include any factual constraints (e.g., "Use Taiwan EPA standards, not US EPA")

---

### 4. Streaming Responses (15 min)

Streaming displays each token as it arrives — the response appears word by word rather than all at once. This makes the app feel faster and more interactive.

```python
with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=512,
    system="You are a Taiwan air quality assistant.",
    messages=[{"role": "user", "content": prompt}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

In Streamlit, use `st.write_stream()` to display a streaming response:

```python
import streamlit as st
import anthropic

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from environment

def stream_response(prompt: str, system: str):
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=512,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        yield from stream.text_stream

# In your Streamlit app:
with st.chat_message("assistant"):
    st.write_stream(stream_response(user_input, system_prompt))
```

---

### 5. Building a Chat Interface in Streamlit (25 min)

Streamlit provides `st.chat_message()` and `st.chat_input()` for building conversational interfaces.

```python
import streamlit as st
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = (
    "You are a Taiwan air quality expert. Explain AQI values, health impacts, "
    "and Taiwan EPA guidelines in plain language. Keep answers concise."
)

st.title("Air Quality Q&A")
st.caption("Ask about air quality data, health effects, or Taiwan EPA standards.")

# Maintain conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Accept new input
if user_input := st.chat_input("Ask a question about air quality..."):
    # Add and display the user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Call Claude and stream the response
    with st.chat_message("assistant"):
        response_text = st.write_stream(
            stream_response(
                user_input,
                SYSTEM_PROMPT,
                st.session_state.messages[:-1],   # conversation history
            )
        )

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
```

`st.session_state` persists values across reruns for the current user session. Without it, the conversation history would reset on every interaction.

---

### 6. Managing API Keys Safely (15 min)

**Never put API keys in source code or commit them to GitHub.**

**Local development — `.env` file:**

```bash
# .env  (add this file to .gitignore)
ANTHROPIC_API_KEY=sk-ant-...
```

```python
# In your Python code
from dotenv import load_dotenv
import os

load_dotenv()   # reads .env into environment variables
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
```

**Streamlit Cloud — `st.secrets`:**

On the Streamlit Cloud dashboard, go to your app → **Settings** → **Secrets** and add:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

In your code:
```python
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
```

**`.gitignore` entries to always include:**
```
.env
*.env
.streamlit/secrets.toml
```

---

### 7. Responsible AI Design (10 min)

An AI feature that answers any question with full confidence is a risk, not a feature. Apply these practices before deploying:

| Practice | Implementation |
|---------|---------------|
| Scope the system prompt | Explicitly refuse out-of-scope requests in the system prompt |
| Show a disclaimer | `st.caption("AI responses may contain errors. Verify important health decisions with a professional.")` |
| Set `max_tokens` | Prevents runaway long responses that are hard to review |
| Display the data source | Show where the underlying data came from, separate from the AI response |
| Log usage (optional) | Store question + response for review; do not log user PII |
| Give users control | Let users clear the chat history; do not persist conversations indefinitely |

---

## Course Connection

| AI feature | Value it adds to your final project |
|-----------|-------------------------------------|
| "What does this AQI mean?" chatbot | Makes raw numbers accessible to non-expert users |
| Automatic summary of top findings | Saves users from reading a long table |
| Follow-up question suggestions | Guides exploration for users new to the data |
| Translation (Chinese ↔ English) | Broadens the accessible audience of your app |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| `anthropic` | Anthropic Python SDK | `pip install anthropic` |
| `python-dotenv` | Load `.env` files into environment | `pip install python-dotenv` |
| `st.chat_message` / `st.chat_input` | Streamlit chat UI components | included with streamlit |
| `st.secrets` | Secure key management on Streamlit Cloud | built into Streamlit |

---

## Assignment

Integrate a Claude API feature into your Streamlit app:

1. Add a chat interface (`st.chat_message`, `st.chat_input`) to your app using the code from Section 5.
2. Write a system prompt specific to your dataset and domain. The system prompt should:
   - Name the role and dataset ("You are an expert on Taiwan earthquake records...")
   - Restrict the scope (what to answer and what to decline)
   - Set a length limit (e.g., under 120 words)
3. Implement streaming responses with `st.write_stream()`.
4. Store your API key in `.env` locally and in `st.secrets` on Streamlit Cloud. Confirm that the `.env` file is listed in `.gitignore` and is not pushed to GitHub.
5. Add a `st.caption()` disclaimer below the chat interface explaining that responses should be verified against the original data.

Push the updated app to GitHub and redeploy. Submit the Streamlit Cloud URL before Week 15.

---

## Resources

- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Messages API reference](https://docs.anthropic.com/en/api/messages)
- [Streaming with the Anthropic SDK](https://docs.anthropic.com/en/api/messages-streaming)
- [Streamlit chat elements documentation](https://docs.streamlit.io/develop/api-reference/chat)
- [Streamlit secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Anthropic usage policies](https://www.anthropic.com/legal/usage-policy)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 15 | Final project workshop — peer review, UI polish, README, rehearsal |
| 16 | **Final milestone:** 10-minute live app presentation |
