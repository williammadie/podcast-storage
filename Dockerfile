FROM python:3.11-alpine

# Set path for further commands
WORKDIR /

# Install Poetry Package Manager
RUN pip install poetry

# Copy source code into container
COPY ./podcast_storage /podcast_storage

# Install project dependencies
RUN touch README.md
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

# Change directory to REST API Subpackage
WORKDIR /podcast_storage

CMD ["poetry", "run", "fastapi", "run", "main.py", "--port", "8000"]