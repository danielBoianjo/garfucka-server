from typing import NoReturn, Union
from flask import request, abort, Flask
from flask.json import jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['POST'])
@cross_origin()
def getAnswer() -> Union[str, NoReturn]:
    if request.method == 'POST':
        if request.get_json() and "data" in request.get_json() and len(request.get_json()) == 1:
            return do_the_logic(request.get_json()["data"])
        else:
            # Not json or doesnt has data attribute or main obj len > 1
            return abort(500)
    else:
        # Not post method
        return abort(500)


def do_the_logic(data: str) -> str:
    print(data)
    return jsonify(data)
