#!/usr/bin/python
import sys
import os
import subprocess
import stat
import argparse
import string
from re import sub, findall
from argparse import RawTextHelpFormatter

closure = '$HOME/bin/closure --compilation_level SIMPLE_OPTIMIZATIONS'

class TextCompressor:
    """String compression class"""
    
    knownTypes = ['css','js','html','php']
    
    re = {
        'htmlScript': '(<script.*>([^<]+)</script>)',
        'htmlStyle': '(<style.*>([^<]+)</style>)',
        'htmlPre': '(<(?:code|pre).*>[^<]+</(?:code|pre)>)',
        'htmlComments': '<!--(.|\s)*?-->',
        'htmlWhitespace1': '[\r\n\t]+',
        'htmlWhitespace2': '([>#])[\s]+([<#])',
        'htmlWhitespace3': '[\s]+',
        'htmlWhitespace4': '\s*=\s*',
        'htmlWhitespace5': '\s*(/?>)',
        
        'php': '(<\?(?:php|=)[^?]+\?>)',
        
        'cssComments1': '//[^\n\r]+',
        'cssWhitespace1': '[\r\n\t\s]+',
        'cssComments2': '/\*.*?\*/',
        'cssWhitespace2': '[\s]*([\{\},;:])[\s]*',
        'cssWhitespace3': '^\s+',
        'cssEnd': ';}'
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
        scripts = findall( self.re['htmlScript'], s)
        s = sub( self.re['htmlScript'], '#@#script#!#', s )
        
        styles = findall( self.re['htmlStyle'], s)
        s = sub( self.re['htmlStyle'],  '#@#style#!#', s )
        
        pres = findall( self.re['htmlPre'], s)
        s = sub( self.re['htmlPre'],    '#@#pre#!#', s )
        
        s = sub( self.re['htmlComments'], '', s )
        
        s = sub( self.re['htmlWhitespace1'], ' ', s )
        s = sub( self.re['htmlWhitespace2'], r'\1\2', s )
        s = sub( self.re['htmlWhitespace3'], ' ', s )
        s = sub( self.re['htmlWhitespace4'], '=', s )
        s = sub( self.re['htmlWhitespace5'], r'\1', s)
        
        for pre in pres:
            s = sub( r'#@#pre#!#', pre[1], s, 1 )
        for style in styles:
            tmp = style[0].replace( style[1], self.compressCss(style[1]) )
            s = sub( r'#@#style#!#', tmp, s, 1 )
        for script in scripts:
            tmp = script[0].replace( script[1], self.compressJs(script[1]) )
            s = sub( r'#@#script#!#', tmp, s, 1 )
        return s
        
    def compressCss(self, s):
        """ Compress CSS string. """
        s = sub( self.re['cssComments1'], '', s )
        s = sub( self.re['cssWhitespace1'], ' ', s )
        s = sub( self.re['cssComments2'], '', s )
        s = sub( self.re['cssWhitespace2'], r'\1', s )
        s = sub( self.re['cssWhitespace3'], '', s )
        s = sub( self.re['cssEnd'], '}', s )
        return s
        
    def compressPhp(self, s):
        """ Compress PHP string. """
        phps = findall( self.re['php'], s)
        s = sub( self.re['php'], '#@#php#!#', s )
        s = self.compressHtml( s )
        
        for php in phps:
            s = sub( r'#@#php#!#', php, s, 1 )
        
        return s
        
    def compressJs(self, s):
        """ Compress JS string. """
        tmp = open('/tmp/wctmp', 'w')
        tmp.write(s)
        tmp.close()
        
        cmd = closure+' < /tmp/wctmp > /tmp/wctmpout'
        
        proc = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=readme, formatter_class=RawTextHelpFormatter)
    parser.add_argument('input', metavar='INFILE', type=argparse.FileType('r'), nargs='*', help='input files', default=sys.stdin)
    parser.add_argument('-o','--output', metavar='OUTFILE', nargs=1, help='output file')
    parser.add_argument('-t','--type', metavar='TYPE', nargs=1, help='force file type')
    parser.add_argument('-f', action='store_true', help='force compression (ignore file modyfication time)')
    parser.add_argument('-d', action='store_true', help='delete source files')

    try:
        args = parser.parse_args()
    except IOError as inst:
        print inst
        exit(1)
    else:
        if type(args.input).__name__ == 'file':
            args.input = [ args.input ]
        if type(args.output).__name__ == 'list':
            args.output = args.output[0]
        args.type = args.type[0] if args.type != None else None

        Packer(args)
