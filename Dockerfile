FROM node:20

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .

EXPOSE 4200

CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]
