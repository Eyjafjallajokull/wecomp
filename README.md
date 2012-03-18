wecomp
======

Pack and compress client-side source code.

Features:

- CSS, JS -- minification and merging files
- HTML -- minification with proper handling of `script` and `style` tags
- PHP -- same as HTML, but PHP code is left untouched

Install
-------

	git clone https://github.com/Eyjafjallajokull/wecomp
	cd wecomp
	sudo easy_install slimit
	for python < 2.7 or < 3.2: sudo easy_install argparse
	sudo ./setup.py install

Configure (optional)
--------------------

By default script uses [slimit](http://slimit.org/) JavaScript compressor. Optionally you can set it to use Google closure compiler, YUI Compressor or whatever you like. Simply create file ~/.wecomp with contents:

	[global]
	# Google Closure compiler
	jscompiler = java -jar $HOME/lib/compiler.jar --compilation_level SIMPLE_OPTIMIZATIONS < %(input)s > %(output)s
	# or for YUI
	# jscompiler = java -jar $HOME/lib/yuicompressor-2.4.6.jar --type js %(input)s > %(output)s

Use
---

	wecomp [-h] [-o OUTFILE] [-t TYPE] [-f] [-d] [INFILE [INFILE ...]]

* `-h, --help` show help message
* `-o OUTFILE, --output OUTFILE` output file
* `-t TYPE, --type TYPE` force file type
* `-f` force compression (ignore file modification time)
* `-d` delete source files


**Examples:**

*	Compress CSS file, work with stdin & stdout:

	_Note:_ When input stream is stdin then `--type` parameter must be set.

		wecomp --type css < style.css > style.min.css
		cat style.css | wecomp --type css
		wecomp style.css > style.min.css
    
*	Compress CSS file, output to file:

	_Note:_ Nothing will be done if output file is newer then input, use `-f` to ignore check.

		wecomp style.css --output style.min.css
    
*	Join and compress JS files, output to file:
	
		wecomp js/* --output main.min.js
  
*	Compress all templates:
	
	Note: PHP code will be left untouched, while compressing everything outside.
	
		for f in `find ./templates/ -name "*php"`; do 
			wecomp -f $f $f
		done

