FROM python:3.11-slim

WORKDIR /app

# Install required system packages (libGL included)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libc-dev libjpeg-dev zlib1g-dev libpng-dev tesseract-ocr libgl1 \
 && rm -rf /var/lib/apt/lists/*

# Copy your application code and dependencies
COPY . /app
COPY dependencies_linux/ /tmp/dependencies/

# Install Python packages offline
RUN pip install --upgrade pip && \
    pip install --no-index --find-links=/tmp/dependencies \
    torch==2.0.1+cpu onnxruntime==1.16.3 \
    fastapi uvicorn numpy==1.26.4 pillow pytesseract opencv-python

# Set command to run FastAPI app
CMD ["python", "main.py"]




