FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json* ./

# Install all dependencies (including dev dependencies for development)
RUN npm install

# Copy source code
COPY . .

EXPOSE 3000

# Start development server with hot reload
CMD ["npm", "run", "dev"]