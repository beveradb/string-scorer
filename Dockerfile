FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# Install poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Navigate to the frontend directory, install dependencies
WORKDIR /app/string_scorer/frontend
COPY string_scorer/frontend/package*.json /app/string_scorer/frontend/
RUN npm install

# Copy the current directory contents into the container at /app
COPY . /app

# Build the frontend
RUN npm run build

# Navigate back to the main app directory
WORKDIR /app

# Expose the port the app runs on
EXPOSE 54321

CMD ["gunicorn", "-b", "0.0.0.0:54321", "-k", "eventlet", "-w", "1", "--timeout", "120", "string_scorer.server:app"]
