FROM python:3.12-slim

WORKDIR /app

COPY . .

# Uv implementation

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv sync --no-cache

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "./src/main.py", "--proxy-headers", "--port", "80"]

# Pip implementation

# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 80

# CMD ["fastapi", "run", "./src/main.py", "--proxy-headers", "--port", "80"]