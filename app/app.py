from flask import Flask, request, render_template

# from app.skysearch import get_answer

app = Flask(__name__)


@app.route("/bot", methods=['GET'])
def start_bot():
    question = request.args['question']
    print("\tgot question", question)
    # return get_answer(question)
    return "Connection failed"


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Engineer'}
    return render_template("viz.html", title='Home', user=user)


@app.route('/viz')
def viz():
    user = {'nickname': 'Engineer'}
    return render_template("viz.html", title='viz', user=user)


if __name__ == '__main__':
    app.run(debug=True)
