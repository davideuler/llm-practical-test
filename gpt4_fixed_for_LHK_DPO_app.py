import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from io import BytesIO
from bs4 import BeautifulSoup  # This is missing from your imports
import pdfplumber

# Define a Pydantic model for the expected request body
class UrlModel(BaseModel):
    url: str

app = FastAPI()

@app.post("/page/")
async def extract_text(body: UrlModel):
    url = body.url
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
        pdf_text += page.extract_text() or ""  # Handle case where extract_text() returns None
    return pdf_text
