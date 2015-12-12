# -*- coding: utf-8 -*-
"""
bottle example of upload file
refer to
0-http://bottlepy.org/docs/dev/tutorial.html#file-uploads
1- https://gist.github.com/Arthraim/994641
2-http://stackoverflow.com/questions/15050064/ \
how-to-upload-and-save-a-file-using-bottle-framework
"""
import os
from bottle import route, run, error, abort, redirect, response, debug
from bottle import get, post,  request, static_file, template

ROOT = os.path.dirname(os.path.abspath(__file__))

@route('/')
@route('/index.html')
def index():
    return '<a herf="/hello">Go to Hello World page</a>'

@route('/hello')
def hello():
    return '<h1>Hello Jeremiah</h1>'

@route('/hello/<name>')
def hello_name(name):
    page = request.GET.get('page', '1')
    return '<h1>Hello %s <br/>(%s)</h1>' % (name, page)

@route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root=ROOT)

@route('/raise_error')
def raise_error():
    abort(404, "error: page not finded")

@route('/redirect')
def redirect_to_hello():
    redirect('/hello')

@route('/ajax')
def ajax_response():
    return {'dictionary': 'you will see ajax response rigth? Content-Type will be "application/json"'}

@error(404)
def error404(error):
    return '404 error !!!'

@get('/upload') # or @route('/upload')
def upload_view():
    return """
    <form action="/upload" method="post" enctype="multipart/form-data">
      Category:     <input type="text" name="category" />
      Select a file: <input type="file" name="upload" />
      <input type="submit" value="Start upload" />
    </form>
    """

@post('/upload')
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed!"

    save_path = ROOT + "/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)

if __name__ == '__main__':
    run(host="localhost", port=8080, debug=1, reload=1)