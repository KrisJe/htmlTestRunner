#!/usr/bin/env python
#runner.py
# -*- coding: utf-8 -*-

import io
import sys
import unittest
import HTMLTestRunner
import git
import time
import os

#---------------------------------------------------------------------------# 
# tool for measuring code coverage of Python program
#---------------------------------------------------------------------------# 
try:
    from coverage import coverage
    coverage_available = True
except ImportError:
    coverage_available = False
    

#---------------------------------------------------------------------------# 
# import unittest classes
#---------------------------------------------------------------------------# 
from test_HTMLTestRunner import *


#Add embedded device repo's here
repo_list =[['S:/github_KrisJe/htmlTestRunner','git.Head "refs/heads/master"','787e204a0f25596507d02113b715a41df37208d2']]



def get_repo_versions():
    u = repo_list[0]    
    r = git.Repo(u[0])       
    u[1] = str(r.head.ref)  
    u[2] = r.head.object.hexsha  
    

    for sub in r.submodules:
        r = git.Repo(u[0] + "/" + sub.path)        
        a = [sub.path, sub.branch_path, r.head.object.hexsha]
        repo_list.append(a)
        
               
            

    
if __name__ == '__main__':

    get_repo_versions()
   
    
    if coverage_available:
        cov = coverage(source=['test_HTMLTestRunner'])
        cov.start() 
        
    newsuite = unittest.TestSuite()
    newsuite.addTests([unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest0),
                       unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest1), 
                       unittest.defaultTestLoader.loadTestsFromTestCase(SampleOutputTestBase), 
                       unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestBasic),
                       unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestHTML),
                       unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestLatin1),
                       unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestUnicode),
                       #...                                    
                       ])

 
    daily_folder = time.strftime("%Y%m%d",time.gmtime(time.time()))
    report_path = "./reports/" + daily_folder
    if (not os.path.exists(report_path)):
        os.mkdir(report_path)
        
    
    fp = open(report_path + '/RegressionReport'   + time.strftime("%H%M%S",time.gmtime(time.time())) + '.html', 'wb')
    
    # Invoke TestRunner  
    #runner = unittest.TextTestRunner(buf)       #DEBUG: this is the unittest baseline
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
                title='<Regression Test Report>',
                description='This is the result of the regression tests performed on the folowing release branch: ',
                rlist = repo_list, verbosity=2
    )
    runner.run(newsuite)
    fp.close()
    
    #---------------------------------------------------------------------------#
    # Code coverage
    #---------------------------------------------------------------------------#      
    if coverage_available:
        cov.stop()
        cov.save()
        print('\nCoverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        basedir += "/reports/" 
        basedir += time.strftime("%Y%m%d",time.gmtime(time.time()))
        #basedir += "/" + os.path.basename(__file__).replace('.py', '')      
        covdir = basedir + "/coverage"        
        #covdir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=covdir)
        print('\nHTML version: file://%s/index.html' % covdir)
        cov.erase()   
    else:
        print("Tipp:\n\tUse 'pip install coverage' to get great code coverage stats")      