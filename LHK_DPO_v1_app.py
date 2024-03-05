## pip install fastapi uvicorn requests pdfplumber
## start the service by :
# uvicorn LHK_DPO_v1_app:app --reload --host 0.0.0.0 --port 8502

import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from io import BytesIO
import requests
import base64
import pdfplumber

#from pdfplumber import PDFPage, PDFTextExtractor

app = FastAPI()

@app.post("/page/")
async def extract_text(request ):
    data = await request.json()
    url = data['url']
    text = extract_html_text(url) if url.endswith('.html') else extract_pdf_text(url)
    return {"extracted_text": text}


def extract_html_text(html_url):
    page = requests.get(html_url).text
    soup = BeautifulSoup(page, 'html.parser')
    text = ' '.join([paragraph.get_text() for paragraph in soup.find_all('p')])
    return text

def extract_pdf_text(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="PDF file not found")

    buffer = BytesIO(response.content)
    pdf = pdfplumber.open(buffer)
    pages = pdf.pages
    pdf_text = ""

    for page in pages:
        pdf_text += page.extract_text()

    return pdf_text

def extract_pdf_text_22(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="PDF file not found")

    byte_pdf = response.content
    buffer = BytesIO(base64.b64decode(byte_pdf))
    pages = PDFPage.extract_text_pages(buffer)
    pdf_text = PDFTextExtractor().extract_text(pages[0])
    return pdf_text

if __name__ == '__main__':
    print("starting service...")
    #app.run(host='0.0.0.0', port=8502, debug=True)
