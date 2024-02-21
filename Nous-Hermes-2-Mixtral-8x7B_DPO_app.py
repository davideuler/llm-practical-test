import requests
from flask import Flask, request, jsonify
from io import BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

app = Flask(__name__)

@app.route('/page/', methods=['POST'])
def extract_content():
    # 获取请求数据
    data = request.get_json()

    # 检查请求数据中是否包含 url 字段
    if 'url' not in data:
        return jsonify({'error': 'Missing url field'}), 400
    print("request url:" + data['url'])

    # 下载网页或 PDF 文件
    response = requests.get(data['url'])

    # 检查响应是否成功
    if response.status_code != 20:
        return jsonify({'error': 'Failed to download content'}), 50

    # 检查响应内容是否为网页或 PDF 文件
    if response.headers.get('content-type') not in ['text/html', 'application/pdf']:
        return jsonify({'error': 'Unsupported content type'}), 400

    # 提取网页或 PDF 文件的内容
    if response.headers.get('content-type') == 'text/html':
        content = extract_text_from_html(response.content)
    elif response.headers.get('content-type') == 'application/pdf':
        content = extract_text_from_pdf(response.content)
    else:
        return jsonify({'error': 'Unsupported content type'}), 400

    # 返回提取的内容
    return jsonify({'content': content})

def extract_text_from_html(html_content):
    # 使用 BeautifulSoup 来提取网页的正文内容
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # 从网页中提取正文内容
    content = soup.find('div', {'class': 'article-content'}).text

    return content

def extract_text_from_pdf(pdf_content):
    # 使用 pdfminer 来提取 PDF 文件的内容
    resource_manager = PDFResourceManager()
    fake_file_handle = BytesIO(pdf_content)
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())

    page_interpreter = PDFPageInterpreter()
    # 处理每一页的内容
    for page in PDFPage.get_pages(fake_file_handle, set()):
        page_interpreter.process_page(page)

    # 从 PDF 文件中提取内容
    text = converter.get_text()
    # 关闭文件句柄
    converter.close()
    fake_file_handle.close()
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502, debug=True)

