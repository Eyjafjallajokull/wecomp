#!/usr/bin/python
import unittest
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath('../lib'))
from wecomp import TextCompressor
from wecomp import Packer

pyexec = 'python ../lib/wecomp.py'

def tearDownClass(cls):
  self.e('rm -f tmp*')

class TestSampleFiles(unittest.TestCase):

  testTypes = TextCompressor.knownTypes
  testTileIn = 'dataSets/in01.css'
  testTileOut = 'dataSets/out01.css'
  

  def setUp(self):
    self.e('rm -f tmp*')
  
  def testTextCompressor(self):
    for file in os.listdir('dataSets'):
      if file.startswith('in'):
        testSetNumber = file[2:file.find('.')]
        testSetType = file[file.find('.')+1:]
        testSetContent = open('dataSets/'+file).read()
        testSetExpectedContent = open('dataSets/out'+testSetNumber+'.'+testSetType).read()
        
        testSetResults = TextCompressor(testSetType).compress(testSetContent)

        self.assertEqual(testSetExpectedContent, testSetResults)

  def testScriptStdOut(self):
    teststring = self.eo(pyexec+' '+self.testTileIn)
    self.checkContent(teststring, self.testTileOut)
  
  def testScriptFileOut(self):
    self.e(pyexec+' '+self.testTileIn+' --output tmp')
    self.assertTrue( os.path.isfile('tmp') )
    self.checkContent(self.r('tmp'), self.testTileOut)
  
  
  def testScriptDelete(self):
    self.e('cp '+self.testTileIn+' tmp.css')
    self.e(pyexec+' -d tmp.css --output tmpOut')
    
    self.assertTrue( not os.path.isfile('tmp.css') )
    self.assertTrue( os.path.isfile('tmpOut') )
    
    self.checkContent(self.r('tmpOut'), self.testTileOut)
    
    
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
