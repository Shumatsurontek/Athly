# Use an official Node runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app/frontend

# Copy package.json and package-lock.json (or yarn.lock) first
# to leverage Docker cache
COPY package*.json ./
# Si vous utilisez yarn, décommentez la ligne suivante et commentez celle d'après
# COPY yarn.lock ./

# Install dependencies
RUN npm install
# Si vous utilisez yarn, décommentez la ligne suivante et commentez celle d'avant
# RUN yarn install

# Copy the rest of the frontend application code
COPY . .

# Expose the port the app runs on (React default is 3000)
EXPOSE 3000

# Command to run the development server
# Pour Next.js utiliser 'next dev' au lieu de 'next start'
CMD ["npm", "run", "dev"] 