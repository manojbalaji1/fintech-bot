from flask import Flask, jsonify, request
from bot import Bot
app = Flask(__name__)
ai_bot = Bot()

@app.route('/question', methods=['GET','POST'])
def hello_world():
    test = request.get_json()
    # answer = ai_bot.answer_user_question(test["question"])
    print(test)
    return jsonify({'message': '{}'.format(test)})


if __name__ == "__main__":
    app.run(host='0.0.0.0')