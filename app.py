from typing import NoReturn, Union
from flask import request, abort, Flask
from flask.json import jsonify
from flask_cors import CORS, cross_origin
from transformers import EncoderDecoderModel, BertTokenizerFast
import wget

url = 'https://github.com/danielBoianjo/garfucka-server/releases/download/beta/pytorch_model.bin'
# url = 'https://github.com/danielBoianjo/garfucka-server/releases/download/beta/config.json'


def config_model(model):
    global tokenizer

    model.config.decoder_start_token_id = tokenizer.cls_token_id
    model.config.eos_token_id = tokenizer.sep_token_id
    model.config.pad_token_id = tokenizer.pad_token_id
    model.config.vocab_size = model.config.encoder.vocab_size

    model.config.max_length = max_length
    model.config.min_length = 1
    model.config.no_repeat_ngram_size = 2
    model.config.early_stopping = True
    model.config.length_penalty = 4.0
    # model.config.num_beams = 4


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
max_length = 16
alephbert_model_name = 'onlplab/alephbert-base'
tokenizer = BertTokenizerFast.from_pretrained(alephbert_model_name)
wget.download(url, "model")
model = EncoderDecoderModel.from_pretrained('model')
config_model(model)


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

    inputs = tokenizer(data, padding="max_length", truncation=True,
                       max_length=max_length, return_tensors="pt")
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask

    outputs = model.generate(input_ids, attention_mask=attention_mask)

    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return jsonify(output_str[0])
