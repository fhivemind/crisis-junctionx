# Use default NodeJS
FROM node:10.15-alpine

# ENV Variables
ENV APPDIR /crisis?

# Install global tools
RUN apk --no-cache --virtual build-dependencies add \
    python \
    make \
    git \
    g++

# Create app tree
WORKDIR $APPDIR
COPY . .

# Install dependencies
RUN npm config set unsafe-perm true \
    && npm install -g forever \
    && npm install --only=prod && apk del build-dependencies \
    && npm cache clean --force

# Build public data
RUN npm run build

# Set permissions
RUN chmod -R 777 $APPDIR/server

# Run server
EXPOSE 3000
CMD ["npm", "run", "server"]