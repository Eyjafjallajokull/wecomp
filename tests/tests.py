import unittest
import subprocess
class TestSampleFiles(unittest.TestCase):
  
  def setUp(self):
    subprocess.Popen('rm tmp', stdout=subprocess.PIPE, shell=True)
  
  def test1(self):
    self.commonFileTest('test1')
    
    
  def commonFileTest(self, test):
    testfile = test+'.html'
    cmd = '../wecomp %s' % testfile
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    teststring = p.communicate()[0]
    expectedString = open(test+'.output.html', 'r').read();
    
    self.assertEqual(teststring, expectedString);

if __name__ == '__main__':
    unittest.main()
