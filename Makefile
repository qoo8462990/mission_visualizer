py_init:
	python3 -m venv ./.pyenv
	./.pyenv/bin/pip install --upgrade pip
	./.pyenv/bin/pip install -r requirements.txt

.PHONY:py_init
