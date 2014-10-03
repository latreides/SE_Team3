#!/usr/bin/env python
import os
os.system('py -2 -m coverage run manage.py test')
os.system('py -2 -m coverage html -d coverage_data --include=./*py')
print 'Coverage Data at: ' + os.path.dirname(os.path.realpath(__file__)) + '/coverage_data/index.html'
