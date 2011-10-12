prefix=/usr
name=wecomp
dataDir=$(prefix)/lib/$(name)
exec=$(prefix)/bin/$(name)

install: uninstall
	mkdir -p $(dataDir) && cp wecomp.py $(dataDir) && ln -s $(dataDir)/wecomp.py $(exec)
    
uninstall:
	rm -rf $(dataDir) $(exec)

test:
	cd tests && python tests.py
