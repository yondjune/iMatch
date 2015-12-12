from fabric.api import local, env, run
#import os
env.shell = "/system/bin/sh -c"
# Local path configuration (can be absolute or relative to fabfile)
#
# Remote server configuration
PY = '/data/data/com.hipipal.qpyplus/files/bin/python'
PYQ = 'root@192.168.2.101'
env.hosts= [PYQ]
env.user = "root"
PYQ_ROOT = '/storage/sdcard0/com.hipipal.qpyplus/projects'
PROJ_NAME = 'imatch'
CRT_PROJ = "%(PYQ_ROOT)s/%(PROJ_NAME)s"% locals()
SCP_UP = "scp *.py %(PYQ)s:%(CRT_PROJ)s/ "% locals()
HTML_UP = "scp *.html %(PYQ)s:%(CRT_PROJ)s/ "% locals()

# Actions define.
#def pushproj(ports='22', name='imatch'):
def pushproj():
    '''scp all .py into Android QPython projects dir
    '''
    print SCP_UP
    local(SCP_UP)

def pushhtml():
    '''scp all .html into Android QPython projects dir
    '''
    print HTML_UP
    local(HTML_UP)

def qpy_run_it(script="hello.py"):
    '''fab qpy_run_it:script=MY.py
    '''
    run('pwd')
    run('ls -la ./')
    #run('export PYTHONHOME=/data/data/com.hipipal.qpyplus/files')
    print '%s %s/%s'% (PY, CRT_PROJ, script)
    #run('%s %s/%s'% (PY, CRT_PROJ, script))
    run('source %s/qpy_profile && %s %s/%s'% (PYQ_ROOT
        , PY
        , CRT_PROJ
        , script
        ))
    #run('%s %s/%s'% (PY, CRT_PROJ, script))

'''main develop loop usage :
$ fab qpy:script=MY_developing.py
so fab will auto:
    - scp all local .py up into mobile QPython projects fold
    - and source right sys. env
    - and call the 'MY_developing.py'
    - so wiil see the script running in mobile desktop ;-)
'''
def qpy(script="hello.py"):
    '''main develop tools, auto upload and running in Android
    '''
    pushproj()
    #qpy_run_it(script)
    env()

def html(script="home.html"):
    """upload html file to Android
    """
    pushhtml()
    env()

def uname():
    '''print Android sys. info.
    '''
    run('uname -a')

def env():
    '''print Android sys. env
    '''
    print 'source %s/qpy_profile'% PYQ_ROOT
    run('env')
    #run('source %s/qpy_profile && env'% PYQ_ROOT)

def genenv(script="gen_env.py"):
    '''gen qpy need env into: /storage/sdcard0/com.hipipal.qpyplus/projects/qpy_profile
    '''
    qpy_run_it(script)
    run('ls -la %s'% CRT_PROJ)
