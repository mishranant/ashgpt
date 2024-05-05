import os
import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


class ChatGPTClone:
    def __init__(self, api_key):
        self.api_key = api_key
        self.messages = []
        openai.api_key = self.api_key

    def send_message(self, message):
        self.messages.append(('user', message))
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      *[
                          {"role": "user" if speaker ==
                              'user' else "assistant", "content": content}
                          for speaker, content in self.messages
            ]],
            max_tokens=1024,
        )
        answer = response.choices[0].message['content'].strip()
        self.messages.append(('bot', answer))
        return answer

    def _build_prompt(self):
        conversation = ""
        for speaker, message in self.messages:
            conversation += f"{speaker.capitalize()}: {message}\n"
        return conversation

    def chat(self):
        @app.route('/', methods=['GET'])
        def home():
            return render_template('index.html')

        @app.route('/send_message', methods=['POST'])
        def get_response():
            user_message = request.json['message']
            answer = self.send_message(user_message)
            return jsonify({'answer': answer})

        app.run(debug=True)

if __name__ == "__main__":
    chatbot = ChatGPTClone(api_key=os.getenv('OPENAI_API_KEY'))
    chatbot.chat()
