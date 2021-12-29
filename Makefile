
clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

test: clean
	@flake8 mailupy
	@pytest --cov=mailupy -s --cov-report=xml --cov-report=term-missing

docs: clean
	@flake8 mailupy
	@sphinx-build -b html ./docs mailupy_docs
