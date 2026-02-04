import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """
You are a neutral conversational agent assisting a psychiatrist.
Your role is to help elicit and clarify the user's experiences.

You must NOT:
- Provide advice or suggestions
- Recommend actions
- Encourage seeking help
- Offer reassurance or validation
- Interpret symptoms
- Label emotions clinically
- Suggest coping strategies

You SHOULD:
- Ask open-ended, neutral questions
- Reflect content factually without interpretation
- Keep responses concise and calm
- Focus on understanding experiences, not changing them

"""

def get_bot_reply(conversation):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in conversation:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    payload = {
        "model": "mistral",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        return "The system is temporarily unavailable."

    data = response.json()
    return data["message"]["content"]

