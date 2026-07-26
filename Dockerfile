FROM python:3.11-slim AS builder

# Build wheels in a separate stage so the runtime image does not carry compilers,
# headers, or git metadata. This usually trims hundreds of MB from the final image.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip wheel --wheel-dir /wheels -r requirements.txt


FROM python:3.11-slim AS runtime

# Keep Streamlit headless and browser-quiet for containerized production runs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false

WORKDIR /app

# Runtime-only shared libraries required by OpenCV/vision/audio dependencies.
# Keeping apt packages out of the builder/runtime cross-over reduces the final
# image size and attack surface.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY requirements.txt ./

# Install from prebuilt wheels to avoid carrying the builder toolchain in the
# final image. This is the main size and reproducibility improvement.
RUN python -m pip install --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

# Non-root runtime user improves container isolation without changing app logic.
RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/.streamlit /app/data /app/logs /app/models \
    && chown -R appuser:appuser /app

# Copy only the runtime surface. Deployment files, local data, venvs, and other
# repository noise are excluded by .dockerignore.
COPY --chown=appuser:appuser app.py ./
COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser assets ./assets
COPY --chown=appuser:appuser .streamlit/config.toml ./.streamlit/config.toml

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
