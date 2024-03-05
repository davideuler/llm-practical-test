# pip install Flask beautifulsoup4 requests pymupdf
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import io

app = Flask(__name__)

@app.route('/page/', methods=['POST'])
def extract_content():
    try:
        data = request.get_json(force=True)
        url = data.get('url')
        if not url:
            return jsonify({"error": "Missing URL"}), 400

        # Check if the URL is a PDF
        if url.lower().endswith('.pdf'):
            content = extract_from_pdf(url)
        else:
            content = extract_from_html(url)

        return jsonify({"content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_from_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

    # Use Beautiful Soup to parse and extract text
    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.extract()
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def extract_from_pdf(url):
    response = requests.get(url)
    response.raise_for_status()

    with fitz.open(stream=io.BytesIO(response.content), filetype="pdf") as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502, debug=True)
