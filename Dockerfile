FROM python:3
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN mkdir /backend
WORKDIR /backend

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VERSION=1.1.11

RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml .
COPY poetry.lock .
COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

CMD /backend/entrypoint.sh
