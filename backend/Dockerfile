# Stage1: Build the application in the `/app` directory.
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Disable Python downloads, because we want to use the system interpreter
# across both images. 
ENV UV_PYTHON_DOWNLOADS=0

# Install dependencies
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Install application
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


# Stage 2: use a final image without uv
FROM python:3.13-slim-trixie

# Setup a non-root user
RUN groupadd --gid 1000 nonroot \
    && useradd --uid 1000 --gid 1000 --create-home nonroot

# Copy the application from the builder
COPY --from=builder --chown=guest:users /app /app
RUN chown nonroot:nonroot /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user to run our application
USER nonroot

# Use `/app` as the working directory
WORKDIR /app

# Run the FastAPIdev by default
# CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "digital_twin:app"]
CMD ["digital-twin"]
