wecomp
======

Pack and compress client-side source code.

Supproted file types: css, js, html, php (templates)

Install
-------

For python < 2.7 or < 3.2 install argparse module:

	easy_install argparse

Then:

	git clone https://github.com/Eyjafjallajokull/wecomp
	cd wecomp
	make install

Configure
---------

Wecomp uses jsmin (by Douglas Crockford) for JS compression. You can 
also setup Google closure compiler, YUI Compressor or whatever you like.
Set it in code:

	jscompiler = '...'

Use
---

	wecomp [-h] [-o OUTFILE] [-t TYPE] [-f] [-d] [INFILE [INFILE ...]]

**Examples:**

*	Compress CSS file, work with stdin, stdout:

	Note: when using stdin, --type must be set

		wecomp --type css < style.css > style.min.css
		cat style.css | wecomp --type css
		wecomp style.css
    
*	Compress CSS file, output to file:

	Note: nothing will be done if output file is newer then input

		wecomp style.css --output style.min.css
    
*	Join and compress JS files, output to file:
	
		wecomp js/* --output main.min.js
  
*	Compress all templates:
	
	Note: PHP code will be left untouched (while compressing everything outside).
	
		for f in `find ./templates/ -name "*php"`; do 
			wecomp -f $f $f
		done

**Optional arguments:**

* *-h, --help* : show help message
* *-o OUTFILE, --output OUTFILE* : output file
* *-t TYPE, --type TYPE* : force file type
* *-f* : force compression (ignore file modyfication time)
* *-d* : delete source files
