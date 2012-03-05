#!/usr/bin/python
import unittest
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from wecomp import TextCompressor
from wecomp import Packer

pyexec = 'python ../wecomp.py'

class TestSampleFiles(unittest.TestCase):

  testTypes = TextCompressor.knownTypes
  
  def setUp(self):
    pass
    #self.e('rm -f tmp')
  
  
  def testTextCompressor(self):
    for file in os.listdir('dataSets'):
      if file.startswith('in'):
        testSetNumber = file[2:file.find('.')]
        testSetType = file[file.find('.')+1:]
        testSetContent = open('dataSets/'+file).read()
        testSetExpectedContent = open('dataSets/out'+testSetNumber+'.'+testSetType).read()
        
        testSetResults = TextCompressor(testSetType).compress(testSetContent)

        self.assertEqual(testSetExpectedContent, testSetResults)

  
  '''
  def testScriptStdOut(self):
    for type in self.testTypes:
      self._testScriptStdOut(type)
  
  def _testScriptStdOut(self, type):
    teststring = self.eo(pyexec+' test.'+type)
    self.checkContent(teststring, type)
  
  
  def testScriptFileOut(self):
    for type in self.testTypes:
      self._testScriptFileOut(type)
      self.setUp()
  
  def _testScriptFileOut(self, type):
    self.e(pyexec+' test.'+type+' --output tmp')
    self.checkContent(self.r('tmp'), type)
    self.assertTrue( os.path.isfile('tmp') )
  
  
  def testScriptDelete(self):
    for type in self.testTypes:
      self._testScriptDelete(type)
      self.setUp()
    
  def _testScriptDelete(self, type):
    self.e('cp test.'+type+' copy.test.'+type)
    self.e(pyexec+' -d copy.test.'+type+' --output tmp')
    
    self.assertTrue( not os.path.isfile('copy.test.'+type), 'aa'+type )
    self.assertTrue( os.path.isfile('tmp') )
    
    self.checkContent(self.r('tmp'), type)
    
    
  def checkContent(self, teststring, type):
    expectedString = self.r('test.output.'+type)
    self.assertEqual(teststring, expectedString)
    
  def e(self,cmd):
    subprocess.Popen(cmd, shell=True).wait()
    
  def eo(self,cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0]
  
  def r(self,file):
    return open(file, 'r').read()
    '''
if __name__ == '__main__':
  unittest.main()
