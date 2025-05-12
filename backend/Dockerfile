FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to create virtual environment in the project directory
RUN poetry config virtualenvs.in-project false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root 

COPY prisma ./prisma/
COPY Makefile ./

RUN make generate

COPY . .

EXPOSE 8000

CMD ["make", "run"]
