from flask import Blueprint
from flask import current_app
from flask import make_response
from flask_wtf import csrf

# 提供静态文件的蓝图
html = Blueprint(name="web_html", import_name=__name__)


# localhost:5000/
# localhost:5000/index.html
# localhost:5000/register.html
# localhost: 5000 / favicon.ico  # 浏览器logo,浏览器会自动请求这个资源


@html.route("/<regex(r'.*'):html_file_name>")
def get_html(html_file_name):
    """提供HTML文件"""

    # 如果html_file_name为空字符串，表示访问的路径是/，请求的是主页

    if not html_file_name:
        html_file_name = "index.html"

    # 如果资源名不是favicon.ico
    if html_file_name != "favicon.ico":
        html_file_name = "html/" + html_file_name

    # 生成csrf_token
    csrf_token = csrf.generate_csrf()

    resp = make_response(current_app.send_static_file(html_file_name))

    # 设置cookie csrf不要设置有效期，防止被窃取，默认为临时会话，即关闭浏览器即失效
    resp.set_cookie("csrf_token", csrf_token)

    return resp
