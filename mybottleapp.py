from bottle import *
from record import *

debug(True)

def read_file(url):
  try:
    from urllib.request import urlopen
  except ImportError:
    from urllib2 import urlopen
    src = data = None
    try:
      src = urlopen(url)
      data = src.read()
    finally:
      if src:
        src.close()
    return data

@route('/', method='GET')
def default():
  return static_file('index.htm', root='static')

@route('/:newxx#new\w+#', method='GET')
def newxx_show(newxx):
  return show_newxx(newxx)

@route('/:newxx/view', method='GET')
def newxx_view(newxx):
  return view_newxx_files(newxx)

@route('/:newxx/:newxxid#\d+#', method='GET')
def newxx_file_show(newxx, newxxid=0):
  return show_newxx_file(newxx, newxxid)

@route('/:newxx/raw/:newxxid#\d+#', method='GET')
def newxx_file_showraw(newxx, newxxid=0):
  return showraw_newxx_file(newxx, newxxid)

@route('/:newxx/view/:id#\d+#', method='GET')
def newxx_file_show(newxx, id=0):
  return view_newxx_file(newxx,id)

@route('/:newxx#new\w+#', method='POST')
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

@route('/:newxx/upload', method='POST')
def newxx_upload(newxx='newxx'):
  filename=request.POST.get('filename',None)
  content=request.POST.get('content',None)
  print "upload: "+newxx+" "+filename

  return upload_newxx(newxx,filename,content)

@route('/:newxx/search', method='POST')
def newxx_upload(newxx='newxx'):
  keywords=request.POST.get('keywords',None)
  print "search: "+newxx+" "+keywords 
  return search_newxx(newxx,keywords)

@route('/:newxx/search/:keywords', method='GET')
def newxx_upload_get(newxx, keywords):
  print "search: "+newxx+" "+keywords
  return search_newxx_get(newxx,keywords)

@route('/:newxx/e/:id#\d+#', method='GET')
def newxx_exec(newxx, id):
  code = showraw_newxx_file(newxx,id)
  exec code
  obj=get_obj_func()
  return obj(request)

@route('/:newxx/e/:id#\d+#', method='POST')
def newxx_exec(newxx, id):
  code = showraw_newxx_file(newxx,id)
  exec code
  obj=get_obj_func()
  return obj(request)

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
  'runtime/repo/wsgi/views/')) 

application=default_app()
