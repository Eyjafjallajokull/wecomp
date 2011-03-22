import unittest
import subprocess
import os

class TestSampleFiles(unittest.TestCase):

  def setUp(self):
    self.e('rm tmp > /dev/null 2>&1')
  
  def testStdOut(self):
    test = 'test1'
    testfile = test+'.html'
    
    teststring = self.eo('../wecomp %s' % testfile)
    
    self.commonFileTest(teststring, test)
  
  def testFileOut(self):
    test = 'test1'
    testfile = test+'.html'
    
    self.e('../wecomp %s --output tmp' % testfile)
    teststring = open('tmp', 'r').read()
    
    self.assertTrue( os.path.isfile('tmp') )
    
  def testFileDelete(self):
    test = 'test1'
    testfile = test+'.html'
    
    self.e('cp %s copy.%s ' % (testfile, testfile))
    self.e('../wecomp -d copy.%s --output tmp' % (testfile))
    teststring = open('tmp', 'r').read()
    
    self.assertTrue( not os.path.isfile('copy.%s' % testfile) )
    self.assertTrue( os.path.isfile('tmp') )
    
    
  def commonFileTest(self, teststring, test):
    expectedString = open(test+'.output.html', 'r').read()
    self.assertEqual(teststring, expectedString)
    
  def e(self,cmd):
    subprocess.Popen(cmd, shell=True).wait()
    
  def eo(self,cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0]
    
if __name__ == '__main__':
    unittest.main()
