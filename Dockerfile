FROM python:3.11-slim

# Install system dependencies required for pyodbc
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    g++ \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft repo for ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV FLASK_APP=web_app.py
ENV DB_TYPE=sqlite
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "web_app:app"]
