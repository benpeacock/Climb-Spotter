import os, sys

activate_this = '/home/jonstjohn/climbspotter/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.append(os.path.dirname(os.path.abspath(__file__))) #  + '/..')

from csapp import app as application

