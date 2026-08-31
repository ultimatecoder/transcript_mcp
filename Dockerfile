FROM python:3.14-slim
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
RUN uv sync --frozen --no-dev
EXPOSE 8000
CMD ["uv", "run", "python", "-m", "transcript_mcp.server"]