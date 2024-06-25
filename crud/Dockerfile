FROM python:3.12
WORKDIR /code
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install
RUN poetry config virtualenvs.create false
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]