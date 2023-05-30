#!/bin/bash
# Helper scripts for working with Docker image and container.
# Author: Dylan Funk
# Email: funk.ml.engineering@gmail.com


# Variables
export IMAGE_NAME="dylan_funk_personal_backend"
CONTAINER_NAME="personal-site-flask"
AWS_REGION="us-east-2"
AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID  # "01234567890" a 12 digit number, from top right of console.
REPOSITORY_PATH="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com" #TODO: set this to the path of your ECS repository
FULLY_QUALIFIED_IMAGE_NAME="$REPOSITORY_PATH/$IMAGE_NAME"
HOST_PORT=9999
CONTAINER_PORT=8080


# Get version from package.json file so can tag the built image with version number.
# If you don't have node installed, you can just hardcode the version number here.
IMAGE_VERSION=3

# Builds the Docker image and tags it with latest version number.
buildImage () {
    echo Building Image Version: $IMAGE_VERSION ...
    cd backend
    docker build -t $IMAGE_NAME:latest -t $IMAGE_NAME:$IMAGE_VERSION -f Dockerfile . \
    && echo Build complete.
}

# Pushes the latest version of the image both with the `latest` and specific version tags
pushImage () {
    docker tag "$IMAGE_NAME:latest" "$FULLY_QUALIFIED_IMAGE_NAME:latest"
    docker tag "$IMAGE_NAME:$IMAGE_VERSION" "$FULLY_QUALIFIED_IMAGE_NAME:$IMAGE_VERSION"
    aws ecr get-login-password --region "$AWS_REGION" | \
        docker login \
        --username AWS \
        --password-stdin "$REPOSITORY_PATH"
    docker push "$FULLY_QUALIFIED_IMAGE_NAME:latest"
    docker push "$FULLY_QUALIFIED_IMAGE_NAME:$IMAGE_VERSION"
}

createRepo () {
    aws ecr create-repository --repository-name $IMAGE_NAME
    echo Created ECR repository: $IMAGE_NAME.
}

runContainer () {
    docker-compose up
}

showImage () {
    echo "Your ECR fully qualified image name is:"
    echo "$FULLY_QUALIFIED_IMAGE_NAME"
}

# Shows the usage for the script.
showUsage () {
    echo "Description:"
    echo "    Builds, runs and pushes Docker image '$IMAGE_NAME'."
    echo ""
    echo "Options:"
    echo "    build: Builds a Docker image ('$IMAGE_NAME')."
    echo "    run: Runs a container based on an existing Docker image ('$IMAGE_NAME')."
    echo "    buildrun: Builds a Docker image and runs the container."
    echo "    createrepo: Creates new ECR repo called '$IMAGE_NAME'"
    echo "    push: Pushs the image '$IMAGE_NAME' to an image repository"
    echo ""
    echo "Example:"
    echo "    ./docker-task.sh build"
    echo ""
    echo "    This will:"
    echo "        Build a Docker image named $IMAGE_NAME."
}

if [ $# -eq 0 ]; then
  showUsage
else
  case "$1" in
      "build")
             buildImage
             ;;
      "run")
             runContainer
             ;;
      "buildpush")
             buildImage
             pushImage
             ;;
      "push")
             pushImage
             ;;
      "createrepo")
             createRepo
             ;;
      "buildrun")
             buildImage
             runContainer
             ;;
      "showimage")
             showImage
             ;;
      *)
             showUsage
             ;;
  esac
fi