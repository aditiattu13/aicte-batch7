import os
from groq import Groq
import gradio as gr

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

system_prompt = """You are an AI Academic Advisor for students.
Ask about their interests, stream, and goals.
Recommend careers, courses, and colleges.
Be friendly, clear, and encouraging."""

def ask_advisor(user_message, history):
    try:
        messages = [{"role": "system", "content": system_prompt}]
        
        for h in history:
            if isinstance(h, dict):
                messages.append({"role": h["role"], "content": h["content"]})
            else:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
        
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

ui = gr.ChatInterface(
    fn=ask_advisor,
    title="🎓 AI Academic Advisor",
    description="Chat with your personal AI Academic Advisor! Ask about careers, courses, and colleges.",
    examples=[
        "I love math and science, what careers should I consider?",
        "I'm in 10th grade, what stream should I choose?",
        "I want to become an engineer, what should I do?",
        "I'm good at arts, what are my career options?"
    ]
)

ui.launch()