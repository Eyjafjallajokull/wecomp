prefix=/usr
name=wecomp
dataDir=$(prefix)/lib/$(name)
exec=$(prefix)/bin/$(name)

install:
	mkdir $(dataDir) && cp wecomp.py jsmin.py $(dataDir) && ln -s $(dataDir)/wecomp.py $(exec)
    
uninstall:
	rm -rf $(dataDir) $(exec)
