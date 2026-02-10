FROM node:22-alpine

WORKDIR /app

COPY ui/svelte-mf/package*.json ./

RUN npm install

COPY ui/svelte-mf/ .

EXPOSE 5174

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5174"]
