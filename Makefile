source := ${wildcard ./arxiv/*.py}
tests := ${wildcard tests/*.py}

.PHONY: run lint

run:
	functions-framework --source "main.py" --target "main"

lint: $(source) $(tests)
	flake8 . --count --max-complexity=10 --statistics
