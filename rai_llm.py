from openai import OpenAI
from rai_voice import speak

# Use OpenRouter's API
client = OpenAI(
    api_key="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",  
    base_url="https://openrouter.ai/api/v1",  
)

def send_to_llm(command):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[
                {"role": "system", "content": "You are a friendly AI assistant named Rai."},
                {"role": "user", "content": command}
            ]
        )
        # Access content correctly
        reply = response.choices[0].message.content.strip()

        print(f"LLM: {reply}")   # Debug
        speak(reply)             # Send to TTS
        return reply

    except Exception as e:
        error_msg = f"Error reaching OpenRouter: {e}"
        print(error_msg)
        speak(error_msg)
        return error_msg
