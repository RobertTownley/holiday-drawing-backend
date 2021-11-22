FROM python:3
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install poetry
RUN rm ~/.cache/poetry
RUN poetry cache clear --all
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

CMD /entrypoint.sh
