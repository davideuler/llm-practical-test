你是一个优秀的 Python 工程师，需要用 Python 实现一个 Rest 服务，用来下载和提取 HTTP 请求条件中指定的 URL 的网页/PDF文件的文本内容。 web 服务接收 POST 的 JSON 数据作为输入, JSON 数据中包含 URL 字段。

HTTP API： /page/ Request Method: POST Request data example： {"url": "https://www.163.com/abc.html"} url 是 HTML 网页的 HTTP 链接。

输出： 对于网页，从网页中提取的正文文本内容（不含 HTML 标签）； 对于 PDF 链接，下载后，解析到 PDF 文件中的内容，返回完整内容。


=======
如何使用 curl 来测试这个服务
curl --http1.0 -X POST -H "Content-Type: application/json" -d '{"url": "https://mirrors.tuna.tsinghua.edu.cn/ctan/info/pdf-forms-tutorial/en/forms.pdf"}' http://localhost:8502/page/

curl -X POST -H "Content-Type: application/json" -d '{"url": "https://web.stanford.edu/~jurafsky/slp3/10.pdf"}' http://localhost:8502/page/

deepseek coder 33b, Snorkel Mistral PairRM-DPO 给的答案修改之后，提供正确的服务:
deepseek-coder-33b-instruct_downloader_app.works.py
Snorkel-Mistral-PairRM-DPO_downloader_app.works.py
