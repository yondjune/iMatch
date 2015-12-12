# -*- coding: utf-8 -*-
#qpy:2
#qpy:webapp:iMatch APP
#qpy:fullscreen
#qpy://127.0.0.1:8080/
'''
Qpython webapp: iMatch
Email: zhangleisuda@gmail.com
Version 1.0
'''
#  全局引用
import os

from bottle import Bottle, ServerAdapter
from bottle import route, run, debug, template, error
from bottle import get, post, request, static_file
from bottle import jinja2_template
from bottle import TEMPLATE_PATH

### 常量定义 ###
ROOT = os.path.dirname(os.path.abspath(__file__))
images = {1:None, 2:None, 3:None}
TEMPLATE_PATH.insert(0, ROOT+"/templates/") # template path setting

"""
由于默认的 bottle 在处理退出时比较难出来，
所以我们引入了自定义的 MyWSGIRefServer，
这能很好实现自我关闭
"""
### qpython web server ###
class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        #sys.stderr.close()
        import threading
        threading.Thread(target=self.server.shutdown).start()
        #self.server.shutdown()
        self.server.server_close()
        print "# Qpython Imatch WebApp"

### Build-in routers ###
def __exit():
    global server
    server.stop()

# 健康监测
def __ping():
    return "ok"

### imatch main function set ###
# webapp routers
app = Bottle()

# Route static files such as images or CSS files then you can got it use <img>
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    img_path = ROOT + "/image"
    return static_file(filepath, root=img_path)

# index route
@app.route('/')
@app.route('/index')
def index():
    return jinja2_template('index.html')

@app.route('/addimage/<id:int>') # first + to add image
def add_image(id):
    return jinja2_template('upload.html', id_item=id)

@app.route('/upload/<id:int>', method='POST') # upload the image
def do_upload_img(id):
    category = "image"
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed!"

    save_path = ROOT + "/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    if not os.path.exists(file_path):
        upload.save(file_path)

    global images
    images[id] = upload.filename
    return jinja2_template('showimg.html', img_dict=images)

### Qpy exit and monitor ###
app.route('/__exit', method=['GET', 'HEAD'])(__exit)
app.route('/__ping', method=['GET', 'HEAD'])(__ping)

### run server ###
try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8080")
    app.run(server=server, reloader=True, debug=True)
except Exception,ex:
    print "Exception: %s" % repr(ex)