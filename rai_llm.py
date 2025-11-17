import os
from openai import OpenAI
from rai_voice import speak 

client = OpenAI(
    api_key="sk-lmstudio-local",  
    base_url="http://localhost:1234/v1", 
)

def send_to_llm(command):
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3-8b", 
            messages=[
                {"role": "system", "content": "You are a friendly AI assistant named Rai. Provide only the direct response, do not include <think> tags or thought processes."},
                {"role": "user", "content": command}
            ],
            temperature=0.7,
        )
        raw_reply = response.choices[0].message.content.strip()

        end_think_tag = "</think>"
        end_index = raw_reply.rfind(end_think_tag)
        if end_index != -1:
            clean_reply = raw_reply[end_index + len(end_think_tag):].strip()
        else:
            clean_reply = raw_reply
        print(f"LLM: {clean_reply}")  
        speak(clean_reply)          
        return clean_reply

    except Exception as e:
        error_msg = f"Error reaching LM Studio: {e}. Is the server running?"
        print(error_msg)
        speak(error_msg)
        return error_msg