from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a supportive student wellbeing assistant."
        },
        {
            "role": "user",
            "content": "A student has reported feeling exhausted and overwhelmed. Write a short encouraging message."
        }
    ],
    max_tokens=100
)

print(response.choices[0].message.content)