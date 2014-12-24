import sae
from bottle import *
from record import *

app = Bottle()
debug(True)

@app.route('/', method='GET')
def default():
    return static_file('index.htm','.')

@app.route('/:newxx#new\w+#', method='GET')
def newxx_show(newxx):
    return show_newxx(newxx)

@app.route('/:newxx/view', method='GET')
def newxx_view(newxx):
    return view_newxx_files(newxx)

@app.route('/:newxx/:newxxid#\d+#', method='GET')
def newxx_file_show(newxx, newxxid=0):
    return show_newxx_file(newxx, newxxid)

@app.route('/:newxx/raw/:newxxid#\d+#', method='GET')
def newxx_file_showraw(newxx, newxxid=0):
    return showraw_newxx_file(newxx, newxxid)

@app.route('/:newxx/view/:id#\d+#', method='GET')
def newxx_file_show(newxx, id=0):
    return view_newxx_file(newxx,id)

@app.route('/:newxx#new\w+#', method='POST')
def newxx_update(newxx):
    print newxx
    who=request.POST.get('who',None)
    what=request.POST.get('what',None)
    #where=request.POST.get('where',None)
    where = request.environ.get('REMOTE_ADDR')
    which=request.POST.get('which',None)
    print who,what,where,which

    id=update_newxx(newxx,who=who,what=what,where=where,which=which)
    return str(id)

@app.route('/:newxx/upload', method='POST')
def newxx_upload(newxx='newxx'):
    filename=request.POST.get('filename',None)
    content=request.POST.get('content',None)
    print "upload: "+newxx+" "+filename

    return upload_newxx(newxx,filename,content)

@app.route('/:newxx/search', method='POST')
def newxx_upload(newxx='newxx'):
    keywords=request.POST.get('keywords',None)
    print "search: "+newxx+" "+keywords

    return search_newxx(newxx,keywords)

@app.route('/:newxx/search/:keywords', method='GET')
def newxx_upload_get(newxx, keywords):
    print "search: "+newxx+" "+keywords
    return search_newxx_get(newxx,keywords)

@app.route('/:newxx/e/:id#\d+#', method='GET')
def newxx_exec(newxx, id):
    code = showraw_newxx_file(newxx,id)
    exec code
    obj=get_obj_func()
    return obj(request)

@app.route('/:newxx/e/:id#\d+#', method='POST')
def newxx_exec(newxx, id):
    code = showraw_newxx_file(newxx,id)
    exec code
    obj=get_obj_func()
    return obj(request)

application = sae.create_wsgi_app(app)
