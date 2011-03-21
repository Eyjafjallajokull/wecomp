import unittest
import subprocess

class TestSampleFiles(unittest.TestCase):
  
  def test1stdout(self):
    test = 'test1'
    testfile = test+'.html'
    cmd = '../wecomp %s' % testfile
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    teststring = p.communicate()[0]
    
    self.commonFileTest(teststring, test)
  
  def test1fileout(self):
    test = 'test1'
    testfile = test+'.html'
    subprocess.Popen('rm tmp > /dev/null 2>&1', shell=True).wait()
    cmd = '../wecomp %s --output tmp' % testfile
    subprocess.Popen(cmd, shell=True).wait()
    teststring = open('tmp', 'r').read()
    
    self.commonFileTest(teststring, test)
    
  def commonFileTest(self, teststring, test):
    expectedString = open(test+'.output.html', 'r').read()
    self.assertEqual(teststring, expectedString)

if __name__ == '__main__':
    unittest.main()
