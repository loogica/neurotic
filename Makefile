test:
	py.test --verbose .

coverage:
	py.test --cov-report html --cov .

full:
	make clean
	python setup.py install
	py.test -v .
	neurotic

clean:
	@rm -rf build/
	@rm -rf build_history/
	@rm -rf dist/
	@rm -rf *egg-info/
	@find . -name '*.py[co,log,dat]' -exec rm -f {} ';'
	@find . -name 'testreportrepository' -exec rm -rf {} ';'
	@find . -name '__pycache__' -exec rm -rf {} ';'
