# FROM python:latest

# WORKDIR /app

# COPY . .

# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8000

# CMD ["fastapi", "run", "./src/main.py"]

FROM python:3.12-slim

WORKDIR /app

COPY . .

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv sync --no-cache

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "./src/main.py"]
