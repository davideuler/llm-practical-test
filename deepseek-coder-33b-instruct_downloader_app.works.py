from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import io

app = Flask(__name__)

@app.route('/page/', methods=['POST'])
def extract_text():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if url.endswith('.pdf'):
        response = requests.get(url)
        pdf_reader = PdfReader(io.BytesIO(response.content))
        text = ''
        page_len = len(pdf_reader.pages)
        for page in range(page_len):
            text += pdf_reader.pages[page].extract_text()
        return jsonify({'text': text}), 200
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return jsonify({'text': text}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502, debug=True)
