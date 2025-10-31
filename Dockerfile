# Use official Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Collect static files (for Whitenoise)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the app using Gunicorn
CMD ["gunicorn", "jobPortal.wsgi:application", "--bind", "0.0.0.0:8000"]
