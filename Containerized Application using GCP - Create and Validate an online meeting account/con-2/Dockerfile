# Use the official Node.js 14 image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the package.json to the working directory
COPY package.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port on which the application will run
EXPOSE 3001

# Define the command to run the application
CMD [ "npm", "start" ]
