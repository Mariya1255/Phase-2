FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Copy requirements from the backend subfolder
COPY ./backend/requirements.txt /code/requirements.txt

# Install dependencies (using the fixed version for better-exceptions)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the contents of the backend folder into /code
COPY ./backend /code

# Run the app (Assuming main.py is inside the backend folder)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
