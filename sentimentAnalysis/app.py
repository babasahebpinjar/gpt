from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask(__name__)
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    result = sentiment_pipeline(data['text'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

