# https://huggingface.co/Salesforce/blip-vqa-base
import os
import torch
from pathlib import Path
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from transformers import BlipProcessor, BlipForQuestionAnswering

app = Flask(__name__)
path = Path(__file__).parent

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
if torch.cuda.is_available():
    model = model.cuda()

dataset = [
    {
        "question": "Does this person look professional?",
        "key": "professional",
        "value": "yes"
    },
    {
        "question": "What is the skin tone of this person?",
        "key": "skin_tone"
    },
    {
        "question": "Does this person have tattoos?",
        "key": "tattoos",
        "value": "yes"
    },
    {
        "question": "What color is this persons hair?",
        "key": "hair_color"
    },
    {
        "question": "Does this person have piercings?",
        "key": "piercings",
        "value": "yes"
    },
    {
        "question": "Is this person smoking a cigarette?",
        "key": "smoking",
        "value": "yes"
    }, 
    {
        "question": "Does this person have a beard?",
        "key": "beard",
        "value": "yes"
    }, 
    {
        "question": "Does this person have glasses?",
        "key": "glasses",
        "value": "yes"
    }, 
    {
        "question": "Is this person bald?",
        "key": "bald",
        "value": "yes"
    }, 
]


@app.route("/")
def index():
    return jsonify({'message': 'Hello World'})
    
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file:
        img = Image.open(BytesIO(file.read())).resize((192, 192))

        data = {}
        for item in dataset:
            question = item['question']
            key = item['key']
            value = item['value'] if 'value' in item else None

            inputs = processor(img, question, return_tensors="pt")

            out = model.generate(**inputs)
            response = processor.decode(out[0], skip_special_tokens=True)
            print(question, response)
            if value is not None:
                data[key] = response == value
            else:
                data[key] = response

        return jsonify(data)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(debug=True, port=port)