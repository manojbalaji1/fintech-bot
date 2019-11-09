from flask import Flask, jsonify, request
from bot import Bot
app = Flask(__name__)
ai_bot = Bot()


@app.route('/question', methods=['GET'])
def hello_world():
    message = request.args.get('message', default = '*', type = str)
    answer = ai_bot.answer_user_question(message)
    print(answer)
    return jsonify({'message': '{}'.format(answer)})


if __name__ == "__main__":
    app.run(host='0.0.0.0')