FROM python:3.11-slim

# Create a non-root user with UID 1000 (Required by Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements and install dependencies as the local user
COPY --chown=user ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the backend files
COPY --chown=user . /app

# Start the FastAPI application on mandatory port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]