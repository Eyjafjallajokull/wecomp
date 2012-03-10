.PHONY: tests
tests:
	cd tests && python tests.py
tests2.6:
	cd tests && python2.6 tests.py


clean:
	rm -rf build dist MANIFEST
	find . -name *.pyc -exec rm -rf {} \;
