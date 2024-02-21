from flask import Flask, request, jsonify
import json
import requests
from html5lib import parse
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route('/page/', methods=['POST'])
def get_page_content():
    data = request.get_json()
    url = data.get('url')

    if url is None:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': str(err)}), 400

    if response.headers.get('content-type') == 'application/pdf':
        pdf_reader = PdfReader(response.content)
        page_count = pdf_reader.getNumPages()
        page_content = pdf_reader.getPage(0).extract_text()
        return jsonify({'content': page_content}), 200
    else:
        html_content = response.content.decode('utf-8')
        html_parser = parse(html_content, treebuilder='lxml')
        body_text = ''.join(html_parser.itertext())
        return jsonify({'content': body_text}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502, debug=True)

