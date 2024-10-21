# 1. Use an official Node.js runtime as the base image
FROM node:18-alpine

# 2. Set the working directory in the container
WORKDIR /dashboard

# 3. Copy package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./

# 4. Install the app dependencies
RUN npm install

# 5. Copy the rest of the application code
COPY . .

# 6. Build the React app for production
RUN npm run dev

# 7. Expose the port your app will run on (default Vite is 3000)
EXPOSE 5173

# 8. Command to run the app in production
CMD ["npm", "run", "dev","preview"]
