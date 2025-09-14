FROM python:3.11-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    USER=appuser

# Create a non-root user
RUN adduser --disabled-password --gecos "" ${USER}

USER ${USER}
ENV PATH="/home/${USER}/.local/bin:${PATH}"

# Set the working directory
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py app.py

ENTRYPOINT python3 app.py

EXPOSE 5000