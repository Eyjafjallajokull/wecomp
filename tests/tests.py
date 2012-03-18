#!/usr/bin/python
import unittest
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath('../lib'))
from wecomp import TextCompressor
from wecomp import Packer

pyexec = 'python ../wecomp'

def tearDownClass(cls):
  self.e('rm -f tmp*')

class TestSampleFiles(unittest.TestCase):

  testTypes = TextCompressor.knownTypes
  testFileIn = 'testTextCompressor/in01.css'
  testFileOut = 'testTextCompressor/out01.css'
  

  def setUp(self):
    self.e('rm -f tmp*')
  
  def testTextCompressor(self):
    '''Test output of TextCompressor module for different types of files'''
    for file in os.listdir('testTextCompressor'):
      if file.startswith('in'):
        testSetNumber = file[2:4]
        testSetType = file[5:]
        testSetContent = open('testTextCompressor/'+file).read()
        testSetExpectedContent = open('testTextCompressor/out'+testSetNumber+'.'+testSetType).read()
        
        testSetResults = TextCompressor(testSetType).compress(testSetContent)

        self.assertEqual(testSetExpectedContent, testSetResults)

  def testScriptMerge(self):
    '''Test output 
    ddir = 'testScriptMerge/'
    files = os.listdir(ddir)
    for file in files:
      if file.find('a.') != -1:
        mergeFiles = []
        testSetNumber = file[2:4]
        testSetType = file[6:]
        for tmp in files:
          if tmp.startswith('in'+testSetNumber) and tmp.endswith(testSetType):
            mergeFiles.append(ddir+tmp)
        
        testSetExpectedContent = open(ddir+'out'+testSetNumber+'.'+testSetType).read()
        
        self.e(pyexec+' '+(' '.join(mergeFiles))+' --output tmp')

        self.assertEqual(testSetExpectedContent, self.r('tmp'))

  def testScriptStdOut(self):
    teststring = self.eo(pyexec+' '+self.testFileIn)
    self.checkContent(teststring, self.testFileOut)
  
  def testScriptFileOut(self):
    self.e(pyexec+' '+self.testFileIn+' --output tmp')
    self.assertTrue( os.path.isfile('tmp') )
    self.checkContent(self.r('tmp'), self.testFileOut)
  
  
  def testScriptDelete(self):
    self.e('cp '+self.testFileIn+' tmp.css')
    self.e(pyexec+' -d tmp.css --output tmpOut')
    
    self.assertTrue( not os.path.isfile('tmp.css') )
    self.assertTrue( os.path.isfile('tmpOut') )
    
    self.checkContent(self.r('tmpOut'), self.testFileOut)
    
    
  def checkContent(self, teststring, outfile):
    expectedString = self.r(outfile)
    self.assertEqual(teststring, expectedString)
    
  def e(self,cmd):
    subprocess.Popen(cmd, shell=True).wait()
    
  def eo(self,cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0]
  
  def r(self,file):
    return open(file, 'r').read()
    
if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestSampleFiles)
  unittest.TextTestRunner(verbosity=2).run(suite)
