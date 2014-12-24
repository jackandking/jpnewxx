# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-09-19 09:51:26.171000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 0.9
# Newpy ID: 131
# Description: sinaapp mysql interface for newxx.

import logging
import os
logger=logging.getLogger(os.path.basename(__file__))
#logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

import MySQLdb
from os import environ
MYSQL_DB = 'newxx'
MYSQL_USER = environ['OPENSHIFT_MYSQL_DB_USERNAME']
MYSQL_PASS = environ['OPENSHIFT_MYSQL_DB_PASSWORD']
MYSQL_HOST_M = environ['OPENSHIFT_MYSQL_DB_HOST']
MYSQL_PORT = int(environ['OPENSHIFT_MYSQL_DB_PORT'])

def show_newxx(newxx):
    sql="select * from `newxx`.`"+newxx+"` order by `id` desc limit 10"
    return get_record(sql)

def show_newxx_file(newxx,newxxid):
    sql="select * from `newxx`.`"+newxx+"_file` where `fileid`="+newxxid+" order by `id` desc limit 1"
    row=get_one_record(sql)
    if row: return "<pre><code>"+row[4]+"</code></pre>"
    return 'ko'

def showraw_newxx_file(newxx,newxxid):
    sql="select * from `newxx`.`"+newxx+"_file` where `fileid`="+newxxid+" order by `id` desc limit 1"
    row=get_one_record(sql)
    if row: return ""+row[4]+""
    return 'ko'

def view_newxx_file(newxx,id):
    sql="select * from `newxx`.`"+newxx+"_file` where `id`="+id
    row=get_one_record(sql)
    if row: return "<pre><code>"+row[4]+"</code></pre>"
    return 'ko'

def view_newxx_files(newxx):
    sql="select * from `newxx`.`"+newxx+"_file` order by `id` desc"
    result=newxx+" sample files:"
    return result+get_filelist(sql)
    row=get_one_record(sql)
    if row: return "<pre><code>"+row[4]+"</code></pre>"
    return 'ko'

def get_raw_filelist(sql):
    connection = MySQLdb.connection(host=MYSQL_HOST_M,port=MYSQL_PORT,user=MYSQL_USER,passwd=MYSQL_PASS)
    connection.select_db(MYSQL_DB)
    connection.query(sql)
    r = connection.store_result()
    row = r.fetch_row()
    result=""
    while row:
        result="%s \nfilename=%s id=%s newxx=%s" % (result,row[0][3],row[0][0],row[0][1])
        row = r.fetch_row()

    return result

def get_filelist(sql):
    connection = MySQLdb.connection(host=MYSQL_HOST_M,port=MYSQL_PORT,user=MYSQL_USER,passwd=MYSQL_PASS)
    connection.select_db(MYSQL_DB)
    connection.query(sql)
    r = connection.store_result()
    row = r.fetch_row()
    result=""
    while row:
        result="%s <br/>\n<id=%s> <a href='%s'>%s</a> %s %s %s" % (result,row[0][0],row[0][1],row[0][1],row[0][2],row[0][3],row[0][5])
        row = r.fetch_row()

    return result

def get_one_record(sql):
    connection = MySQLdb.connection(host=MYSQL_HOST_M,port=MYSQL_PORT,user=MYSQL_USER,passwd=MYSQL_PASS)
    connection.select_db(MYSQL_DB)
    connection.query(sql)
    r = connection.store_result()
    row = r.fetch_row()
    if row: return row[0]
    return None

def get_record(sql):
    connection = MySQLdb.connection(host=MYSQL_HOST_M,port=MYSQL_PORT,user=MYSQL_USER,passwd=MYSQL_PASS)
    connection.select_db(MYSQL_DB)
    connection.query(sql)
    r = connection.store_result()
    row = r.fetch_row()
    if row: result=row[0][0]
    else: result="0"
    while row:
        result="%s <br/> %s" % (result,row[0])
        row = r.fetch_row()

    return result

#which version
#who is the author
#what samples
#where is the host
def update_newxx(newxx,which,who,what,where):
    return update_record(newxx,which,who,what,where)

def update_record(table,which,who,what,where):
    connection = MySQLdb.connection(host=MYSQL_HOST_M,port=MYSQL_PORT,user=MYSQL_USER,passwd=MYSQL_PASS)
    connection.select_db(MYSQL_DB)
    try:
        connection.query("INSERT INTO `newxx`.`"+table+"` ( `who`, `which`, `what`, `where`) VALUES ( '"+who+"', '"+which+"', '"+what+"', '"+where+"')")
        return connection.insert_id()
    except:
        return 0

def upload_newxx(newxx,filename,content):
    logger.debug("upload_newxx: %s %s %s",newxx,filename,content)
    import re
    newxxid=0
    m=re.search('# New'+newxx[3:]+' ID: (\d+)',content)
    if m:
        newxxid=m.group(1)
        logger.debug("found newxxid: %s",newxxid)
    if newxxid == 0: 
      logger.error("no newxxid found in <%s>",filename)
      return 'ko: no '+newxx+' id'
    author=None
    m=re.search('# Author: (.*)',content)
    if m:
        author=m.group(1)
    if author is None: return 'ko: no author'
    content=str(MySQLdb.escape_string(content))
    return upload_file(newxx+'_file',newxxid,author,filename,content)

def search_newxx(newxx,keywords):
    logger.debug("search_newxx: %s %s",newxx,keywords)
    keywords=str(MySQLdb.escape_string(keywords))
    sql="select * from `newxx`.`"+newxx+"_file` where `content` like '%"+keywords+"%'"
    try:
      return get_raw_filelist(sql)
    except NameError, e:
      print e
      return e
    except:
      import sys
      return "Unexpected error:", sys.exc_info()[0]

def search_newxx_get(newxx,keywords):
    logger.debug("search_newxx: %s %s",newxx,keywords)
    keywords=str(MySQLdb.escape_string(keywords))
    sql="select * from `newxx`.`"+newxx+"_file` where `content` like '%"+keywords+"%'"
    try:
      return get_filelist(sql)
    except NameError, e:
      print e
      return e
    except:
      import sys
      return "Unexpected error:", sys.exc_info()[0]

def upload_file(table,newxxid,author,filename,content):
    connection = MySQLdb.connection(host=MYSQL_HOST_M,port=MYSQL_PORT,user=MYSQL_USER,passwd=MYSQL_PASS)
    connection.select_db(MYSQL_DB)
    try:
        connection.query("INSERT INTO `newxx`.`"+table+"` ( `fileid`, `author`, `filename`, `content`) VALUES ( '"+newxxid+"', '"+author+"', '"+filename+"', '"+content+"')")
        return 'ok'
    except NameError, e:
        print e
    except:
        import sys
        print "Unexpected error:", sys.exc_info()[0]
        return 'ko'

def info():
        return ["DB:%s<br>USER:%s<br>PASS:%s<br>HOST:%s<br>PORT:%s"%(MYSQL_DB,MYSQL_USER,MYSQL_PASS,MYSQL_HOST_M,MYSQL_PORT)]

if __name__ == '__main__':
		print ""


