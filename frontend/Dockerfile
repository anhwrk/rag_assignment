# Use an official Node.js image as the base image
FROM node:22-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Set the working directory in the container to /app
WORKDIR /app

# Copy the package.json and yarn.lock files to the container
COPY package*.json yarn.lock ./

# Install dependencies
RUN yarn install --ignore-engines

# Copy the rest of the application code to the container
COPY . .

# Build the application
RUN yarn build

# Set environment variables
ENV NODE_ENV=production

# Expose port 3000
EXPOSE 3000

# Start the application
CMD [ "yarn", "start" ]