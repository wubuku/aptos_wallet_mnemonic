FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/aptos:${PATH}"

# Install common development tools and dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    vim \
    software-properties-common \
    build-essential \
    ca-certificates \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry for Python dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Create directory for Aptos CLI
WORKDIR /opt/aptos

# Download and install Aptos CLI
RUN wget https://github.com/aptos-labs/aptos-core/releases/download/aptos-cli-v3.5.0/aptos-cli-3.5.0-Ubuntu-22.04-x86_64.zip && \
    unzip aptos-cli-3.5.0-Ubuntu-22.04-x86_64.zip && \
    chmod +x aptos && \
    rm aptos-cli-3.5.0-Ubuntu-22.04-x86_64.zip

# Install Node.js (latest LTS version 20.x)
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Verify installations
RUN python3 --version && \
    poetry --version && \
    node --version && \
    npm --version && \
    /opt/aptos/aptos --version

# Set up a project directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction

# Expose port for potential future Node.js service
EXPOSE 3000

# Set a default command (can be overridden at runtime)
CMD ["/bin/bash"] 