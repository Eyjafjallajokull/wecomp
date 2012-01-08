wecomp
======

Pack and compress client-side source code.

Features:

- CSS, JS -- minification and merging files
- HTML -- minification with proper handling of `script` and `style` tags
- PHP -- same as HTML, but PHP code is left untouched

Install
-------

1.	Get code: `git clone https://github.com/Eyjafjallajokull/wecomp`
1.	By default script uses [slimit](http://slimit.org/) JavaScript compressor. To install this module simply do: `sudo easy_install slimit`

	-- or --
	
	You can also configure script to use Google closure compiler, YUI Compressor or whatever you like. Simply open `wecomp.py`, comment line:

		jscompiler = 'internal'

	then set up your own compressing command, for example:

		# Google closure compiler
		jscompiler = 'java -jar $HOME/bin/closureCompiler.jar --compilation_level SIMPLE_OPTIMIZATIONS < %(input)s > %(output)s'
		# YUI compressor
		jscompiler = 'java -jar $HOME/bin/yuicompressor-2.4.6.jar --type js %(input)s > %(output)s'


2.	For python < 2.7 or < 3.2 install argparse module: `sudo easy_install argparse`
	
3.	Finally: `sudo make install`


Use
---

	wecomp [-h] [-o OUTFILE] [-t TYPE] [-f] [-d] [INFILE [INFILE ...]]

* `-h, --help` : show help message
* `-o OUTFILE, --output OUTFILE` : output file
* `-t TYPE, --type TYPE` : force file type
* `-f` : force compression (ignore file modification time)
* `-d` : delete source files


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

**Optional arguments:**

	wecomp [-h] [-o OUTFILE] [-t TYPE] [-f] [-d] [INFILE [INFILE ...]]

* *-h, --help* : show help message
* *-o OUTFILE, --output OUTFILE* : output file
* *-t TYPE, --type TYPE* : force file type
* *-f* : force compression (ignore file modification time)
* *-d* : delete source files
