# Name of the Docker image
IMAGE_NAME=forensic-log-tester

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

test:
	docker run --rm $(IMAGE_NAME)

run_test:
	# Build the Docker image
	docker build -t $(IMAGE_NAME) .
	# Run the container and execute tests
	docker run --rm $(IMAGE_NAME)

# Clean up dangling Docker images (optional)
clean:
	docker image prune -f