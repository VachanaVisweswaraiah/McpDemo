FROM python:3.11-slim

WORKDIR /demo

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY 02_mcpcrashcourse/mcpserver/server.py .
COPY 02_mcpcrashcourse/mcpserver/client-sse.py .

EXPOSE 8000

CMD ["uv", "run", "server.py"]
