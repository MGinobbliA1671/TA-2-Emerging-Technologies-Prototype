from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder='Frontend')

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def index():
    return render_template('botchat.html')


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    response = get_chat_response(msg)
    return jsonify({"response": response})


def get_chat_response(text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
    "model": "llama3-70b-8192",
    "messages": [
        {
            "role": "system",
            "content": (
                "You are a highly motivational and positive chatbot. "
                "Your job is to uplift the user, give encouragement, and inspire them like a supportive life coach. "
                "Respond warmly, with short motivational quotes, affirmations, or cheerful messages. "
                "Vary your response length, but favor short and snappy messages to keep the user energized."
            )
        },
        {
            "role": "user",
            "content": text
        }
    ],
    "max_tokens": 250,
    "temperature": 0.6
   }

    try:
        response = requests.post(GROQ_API_URL.strip(), json=payload, headers=headers)
        data = response.json()

        print("Groq API Response:", data)

        if 'choices' in data and len(data['choices']) > 0:
            return data['choices'][0]['message']['content']
        else:
            return f"API Error: {data.get('error', 'Unexpected response format.')}"
    except Exception as e:
        return f"Exception: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
    