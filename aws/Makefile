SHELL := /bin/bash

.venv:
	python -m venv .venv

install: .venv
	source .venv/bin/activate && pip install -r requirements.txt
	echo "Please use ./run.sh to run the application"

clean:
	$(RM) -rf .venv
