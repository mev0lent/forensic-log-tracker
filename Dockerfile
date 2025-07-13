FROM ubuntu:latest
LABEL authors="YoBiKhu"

ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy everything from the root (build context) into the container
COPY ./ ./

# Install dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Run tests
CMD ["python3", "-m", "pytest", "--cov=.", "-s", "test"]