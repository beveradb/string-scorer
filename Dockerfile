FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 54321

# Command to run the app using the poetry entrypoint
CMD ["poetry", "run", "string-scorer"]
