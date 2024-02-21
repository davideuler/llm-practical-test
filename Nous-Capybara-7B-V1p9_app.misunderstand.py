mport requests
import json
import os
import uuid
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/page', methods=['POST'])
def page():
    data = request.get_json()
    url = data.get('url')

    if url is None:
        return 'Invalid URL', 400

    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.headers['content-type'] == 'application/pdf':
                pdf_filename = str(uuid.uuid4()) + '.pdf'
                with open(pdf_filename, 'wb') as f:
                    f.write(response.content)
                return send_file(pdf_filename, as_attachment=True)
            else:
                text = response.text
                return text
        else:
            return 'Error downloading the URL', response.status_code
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)

