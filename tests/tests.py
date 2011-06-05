#!/usr/bin/python
import unittest
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from wecomp import TextCompressor
from wecomp import Packer

pyexec = 'python ../wecomp'

class TestSampleFiles(unittest.TestCase):

  testTypes = TextCompressor.knownTypes
  
  def setUp(self):
    self.e('rm tmp > /dev/null 2>&1')
  
  
  def testModuleCompression(self):
    for type in self.testTypes:
      self._testModuleCompression(type)
  
  def _testModuleCompression(self, type):
    tc = TextCompressor(type)
    teststring = tc.compress( self.r('test.'+type ) )
    
    self.checkContent(teststring, type)
  
  
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
    
if __name__ == '__main__':
    unittest.main()
