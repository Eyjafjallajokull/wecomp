tests:
	cd tests && python tests.py
.PHONY: tests

clean:
	rm -rf build MANIFEST
	find . -name *.pyc -exec rm -rf {} \;
