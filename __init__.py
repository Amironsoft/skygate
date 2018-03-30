from flask import Flask, request, render_template
from skysearch import get_answer

app = Flask(__name__)


@app.route("/bot", methods=['GET'])
def start_bot():
    question = request.args['question']
    print("\tgot question", question)
    answers = get_answer(question)
    return answers


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Engineer'}
    return render_template("index.html", title='Home', user=user)


@app.route('/viz')
def viz():
    user = {'nickname': 'Engineer'}
    return render_template("viz.html", title='viz', user=user)


@app.route('/data', methods=['GET'])
def get_data():
    print("found data request")
    file = request.args['file']
    print('url_rule:', file)
    file_extension = file.split(".")[-1]
    allowed_extensions = ["xml", "tsv", "txt", "html", "json"]

    if file_extension in allowed_extensions:
        local_file = file.replace("___", "/")
        print(local_file)
        return app.send_static_file(local_file)
    else:
        return "file not found"


if __name__ == '__main__':
    app.run(debug=True)
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config["CACHE_TYPE"] = "null"
