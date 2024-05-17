PYTHON := python3.11
VENV_PATH := .venv

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    ENV_PYTHON := $(VENV_PATH)/Scripts/python.exe
    BIN_PATH := $(VENV_PATH)/Scripts
else
    ENV_PYTHON := $(VENV_PATH)/bin/python
    BIN_PATH := $(VENV_PATH)/bin
endif

# after charset-normalizer 3.0.1 released, poetry install failed, make version as 2.1.1
init:
	$(PYTHON) -m venv $(VENV_PATH)
	$(BIN_PATH)/pip install cffi==1.16.0
	$(BIN_PATH)/pip install charset-normalizer==2.1.1
	$(BIN_PATH)/pip install poetry==1.2.2
	$(BIN_PATH)/pip install pre-commit==2.20.0
	$(BIN_PATH)/pre-commit install


install:
	$(BIN_PATH)/pip install cffi==1.16.0
	$(BIN_PATH)/pip install charset-normalizer==2.1.1
	$(BIN_PATH)/pip install poetry==1.2.2
	$(BIN_PATH)/poetry config virtualenvs.path $(VENV_PATH)
	$(BIN_PATH)/poetry config virtualenvs.create false
	$(BIN_PATH)/poetry config --list
	$(BIN_PATH)/poetry config experimental.new-installer false
	$(BIN_PATH)/poetry show
	$(BIN_PATH)/poetry install


fmt:
	${ENV_PYTHON} -m ruff format ./app


check:
	${ENV_PYTHON} -m mypy ./app
	${ENV_PYTHON} -m ruff format ./app
	${ENV_PYTHON} -m ruff check ./app

debug:
	$(BIN_PATH)/uvicorn app.api.main:app --reload --port 4399

server:
	$(BIN_PATH)/uvicorn app.api.main:app --port 5000 --workers 4

task:
	${ENV_PYTHON} -m celery --app app.task worker --concurrency=1

cron:
	${ENV_PYTHON} -m  celery -A app.task beat -l INFO
