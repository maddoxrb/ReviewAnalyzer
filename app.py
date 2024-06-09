from flask import Flask, request, jsonify, send_from_directory
from wordcloud_generator import generate_word_cloud
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/generate-wordcloud', methods=['GET'])
def wordcloud():
    result = generate_word_cloud()
    return jsonify(result)

@app.route('/static/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/analyze')
def analyze():
    return send_from_directory('', 'analyze.html')

@app.route('/about')
def about():
    return send_from_directory('', 'about.html')

@app.route('/jacket')
def jacket():
    return send_from_directory('', 'jacket.html')

if __name__ == '__main__':
    app.run(debug=True)
