FROM debian:bookworm as builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --locked --no-install-project --no-dev

COPY main.py /app/
COPY src/ /app/src/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --locked --no-dev

COPY .chainlit/ /app/.chainlit
COPY public/ /app/public/


FROM debian:bookworm-slim

WORKDIR /app
COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]
