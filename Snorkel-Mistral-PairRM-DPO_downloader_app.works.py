import os
import io
import json
import requests
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import PyPDF2

app = Flask(__name__)

@app.route('/page/', methods=['POST'])
def process_url():
    data = request.get_json()
    url = data.get('url')

    try:
        if url.endswith('.pdf'):
            response = requests.get(url)
            pdf_text = extract_text_from_pdf(response.content)
        else:
            response = requests.get(url)
            html_content = response.text
            pdf_text = extract_text_from_html(html_content)

        return jsonify({'text': pdf_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    text = soup.get_text()
    return ' '.join(text.split())

def extract_text_from_pdf(pdf_bytes):
    pdf_file = open('temp.pdf', 'wb')
    pdf_file.write(pdf_bytes)
    pdf_file.close()

    pdf_reader = PyPDF2.PdfReader(open('temp.pdf', 'rb'))
    text = ''
    pages_len = len(pdf_reader.pages)
    for page_num in range(pages_len):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()

    os.remove('temp.pdf')
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502, debug=True)

