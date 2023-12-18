import os
import aiohttp
import asyncio
from pathlib import Path
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from fastai.vision.all import load_learner, PILImage

app = Flask(__name__)
path = Path(__file__).parent
current_directory = os.getcwd()
print(f"Path is {path}")
print("Current Working Directory:", current_directory)

export_file_url = os.environ.get('MODEL_URL')
export_file_name = 'chubby.pkl'


async def download_file(url, dest):
    if dest.exists():
        print(f"File already exists: {dest}")
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                with open(dest, 'wb') as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                file_size = os.path.getsize(dest)
                print(f"File downloaded: {dest}, Size: {file_size} bytes")
                if file_size == 0:
                    print("Warning: Downloaded file size is 0 bytes")
            else:
                print(f"Failed to download file, status code: {response.status}")

async def setup_learner():
    filepath = path / export_file_name
    await download_file(export_file_url, filepath)
    try:
        file_exists = os.path.exists(filepath)
        try:
            learn = load_learner(filepath)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")

        print("model loaded")
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
model = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


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
        prediction = model.predict(PILImage.create(img))
        
        # Extracting the predicted category and probabilities
        predicted_category = prediction[0]
        probabilities = prediction[2]
        
        # Finding the index of the predicted category
        category_index = model.dls.vocab.o2i[predicted_category]

        # Extracting the probability for the predicted category
        confidence = probabilities[category_index].item() * 100  # Convert to percentage

        return jsonify({'category': predicted_category, 'confidence': f'{confidence:.2f}'})


if __name__ == '__main__':
    app.run(debug=True, port=8081)