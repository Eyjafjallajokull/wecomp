#!/usr/bin/python
import sys
import os
import subprocess
import stat
import argparse
import string
from re import sub, findall
from ConfigParser import RawConfigParser

__version__ = '0.2'


config = RawConfigParser()
config.add_section('global')
config.set('global','jscompiler','internal')
config.read(os.environ['HOME']+'/.wecomp')


class TextCompressor:
    """String compression class"""
    
    knownTypes = ['css','js','html','php']
    
    re = {
        'htmlScript': ('(?s)(<script[^>]*>(.*?)</script>)', '#@#script#!#'),
        'htmlStyle': ('(<style.*>([^<]+)</style>)', '#@#style#!#'),
        'htmlPre':   ('(<pre.*>[^<]+</pre>)', '#@#pre#!#'),
        'htmlComments': ('<!--(.|\s)*?-->', ''),
        'htmlWhitespace1': ('[\r\n\t]+', ' '),
        'htmlWhitespace2': ('([>#])[\s]+([<#])', r'\1 \2'),
        'htmlWhitespace3': ('[\s]+', ' '),
        'htmlWhitespace4': ('\s*=\s*', '='),
        'htmlWhitespace5': ('\s*(/?>)', r'\1'),
        
        'php': ('(?s)(<\?php.*?\?>)', '#@#php#!#'),
        'php2': ('(?s)(<\?=.*?\?>)', '#@#php2#!#'),
        
        'cssComments1': ('//[^\n\r]+', ''),
        'cssWhitespace1': ('[\r\n\t\s]+', ' '),
        'cssComments2': ('/\*.*?\*/', ''),
        'cssWhitespace2': ('[\s]*([\{\},;:])[\s]*', r'\1'),
        'cssWhitespace3': ('^\s+', ''),
        'cssEnd': (';}', '}')
    }
    
    def __init__(self, type):
        """ Init compression with a given type. """
        if not type in self.knownTypes:
            print "unknown file type"
            exit(3)
        self.type = type
            
    def compress(self, input):
        """ Compress string. """
        if self.type == 'html':
            return self.compressHtml(input)
        if self.type == 'js':
            return self.compressJs(input)
        if self.type == 'css':
            return self.compressCss(input)
        if self.type == 'php':
            return self.compressPhp(input)
        
    def compressHtml(self, s):
        """ Compress HTML string. """
        (s, scripts) = self.cut(s, 'htmlScript')
        (s, styles) = self.cut(s, 'htmlStyle')
        (s, pres) = self.cut(s, 'htmlPre')
        
        s = self.replace(s, 'htmlComments')
        s = self.replace(s, 'htmlWhitespace1')
        s = self.replace(s, 'htmlWhitespace2')
        s = self.replace(s, 'htmlWhitespace3')
        s = self.replace(s, 'htmlWhitespace4')
        s = self.replace(s, 'htmlWhitespace5')
        
        for pre in pres:
            s = sub( self.re['htmlPre'][1], pre, s, 1 )
        for style in styles:
            tmp = style[0].replace( style[1], self.compressCss(style[1]) )
            s = sub( self.re['htmlStyle'][1], tmp, s, 1 )
        for script in scripts:
            tmp = script[0].replace( script[1], self.compressJs(script[1]) )
            s = sub( self.re['htmlScript'][1], tmp, s, 1 )
        return s
        
    def compressCss(self, s):
        """ Compress CSS string. """
        s = self.replace(s, 'cssComments1')
        s = self.replace(s, 'cssWhitespace1')
        s = self.replace(s, 'cssComments2')
        s = self.replace(s, 'cssWhitespace2')
        s = self.replace(s, 'cssWhitespace3')
        s = self.replace(s, 'cssEnd')
        return s
        
    def compressPhp(self, s):
        """ Compress PHP string. """
        (s, phps) = self.cut(s, 'php')
        (s, php2s) = self.cut(s, 'php2')
        
        s = self.compressHtml( s )
        
        for php in phps:
            s = sub( self.re['php'][1], php, s, 1 )
        for php in php2s:
            s = sub( self.re['php2'][1], php, s, 1 )
        
        return s
        
    def compressJs(self, s):
        """ Compress JS string. """
        jscompiler = config.get('global', 'jscompiler')
        if jscompiler == 'internal':
            from slimit import minify
            s = minify(s, mangle=False)
            
        else:
            tmp = open('/tmp/wctmp', 'w')
            tmp.write(s)
            tmp.close()
            
            cmd = jscompiler % {'input':'/tmp/wctmp', 'output':'/tmp/wctmpout'}
            proc = subprocess.Popen([cmd], 
                shell=True, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
            for line in proc.stdout.readlines():
                sys.stdout.write(line)
            for line in proc.stderr.readlines():
                sys.stdout.write(line)
            
            proc.wait()
            if proc.returncode != 0:
                exit(1)
                
            tmp = open('/tmp/wctmpout', 'r')
            s = tmp.read().strip()
            tmp.close()
            
        return s
    
    def replace(self, string, name):
        """ Do the funky replace on 'string' using 'name' RegExp """
        return sub( self.re[name][0], self.re[name][1], string )
    
    def cut(self, string, name):
        """ Cut from 'string' using 'name' RegExp, return new string and matches """
        tmp = findall( self.re[name][0], string )
        string = sub( self.re[name][0], self.re[name][1], string, 0 )
        return (string, tmp)

class Packer:
    fileType = None
    input = []
    output = None
    force = False
    delete = False
    
    def __init__(self, args):
        output = args.output
        self.input = args.input or []
        self.type = args.type or self.input[0].name.split('.')[-1]
        self.force = args.f or False
        self.delete = args.d or False
        
        for file in self.input[1:]:
            if not file.name.endswith(self.type):
                print "files must be same type"
                exit(2)
                
        if output!=None:
            outputMtime = 0
            try:
                outputMtime = os.stat(output).st_mtime
            except OSError:
                pass
            
            do = False
            if self.force:
                do = True
            else:
                for file in self.input:
                    inputMtime = os.stat(file.name).st_mtime
                    if inputMtime > outputMtime:
                        do = True
            
            if not do:
                print "files up to date, skipping"
                exit(0)
        else:
            self.output = sys.stdout
        
        tc = TextCompressor(self.type)
        compressed = tc.compress( self.readInput() )

        if self.delete==True:
            for file in self.input:
                os.remove(file.name)            

        if output!=None:
          self.output = open(output, 'w')
        
        self.output.write( compressed )
        
    def readInput(self):
        s = ''
        for file in self.input:
            s += file.read()
        return s



def main():
    s = __file__
    s = s[s.rfind('/')+1:]
    readme = """
Pack and compress client-side source code.
Currently supported file formats: %(types)s

Note: Google Closure compiler is used to compress JS. (set path in source)
Note: PHP code will be left untouched (while compressing everything outside).

Examples:
  Compress CSS file, work with stdin, stdout:
    Note: when using stdin, --type must be set
    %(sc)s --type css < style.css > style.min.css
    cat style.css | %(sc)s --type css
    %(sc)s style.css
    
  Compress CSS file, output to file:
    Note: nothing will be done if output file is newer then input
    %(sc)s style.css --output style.min.css
    
  Join and compress JS files, output to file:
    %(sc)s js/* --output main.min.js
  
  Compress all templates:
    for f in `find ./templates/ -name "*php"`; do 
      %(sc)s -f $f $f
    done
    """ % { "types": TextCompressor.knownTypes, "sc": s}


    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        description=readme, 
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('input', 
        metavar='INFILE', type=argparse.FileType('r'), nargs='*', 
        help='input files', default=sys.stdin)
    parser.add_argument('-o','--output', 
        metavar='OUTFILE', nargs=1, help='output file')
    parser.add_argument('-t','--type', 
        metavar='TYPE', nargs=1, help='force file type')
    parser.add_argument('-f', 
        action='store_true', help='force compression (ignore file modyfication time)')
    parser.add_argument('-d', 
        action='store_true', help='delete source files')

    try:
        args = parser.parse_args()
    except IOError as inst:
        print inst
        exit(1)
    
    if type(args.input).__name__ == 'file':
        args.input = [ args.input ]
    if type(args.output).__name__ == 'list':
        args.output = args.output[0]
    args.type = args.type[0] if args.type != None else None


    Packer(args)


if __name__ == "__main__":
    main()
