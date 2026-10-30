
# Docker image mirror
FROM mirror-docker.runflare.com/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Configure Liara Debian mirrors
RUN set -eux; \
    find /etc/apt -type f \( -name "*.sources" -o -name "*.list" \) \
        -exec sed -i \
        -e 's|https\?://deb.debian.org/debian-security|http://linux-mirror.liara.ir/repository/debian-security|g' \
        -e 's|https\?://security.debian.org/debian-security|http://linux-mirror.liara.ir/repository/debian-security|g' \
        -e 's|https\?://deb.debian.org/debian|http://linux-mirror.liara.ir/repository/debian|g' \
        {} +; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates; \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/

RUN pip config set global.index-url https://mirror-pypi.runflare.com/simple \
    && pip config set global.trusted-host mirror-pypi.runflare.com \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Configure Liara npm mirror and build frontend
WORKDIR /app/frontend

RUN npm config set registry https://package-mirror.liara.ir/repository/npm/ \
    && npm install \
    && npm run build

# Return to application directory
WORKDIR /app

EXPOSE 8000

# Start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
