#develop stage
FROM node:16 as vue-develop-stage

WORKDIR /frontend

COPY ./Neptune-UI/package*.json ./
RUN npm install --legacy-peer-deps

COPY ./Neptune-UI/ .
RUN npm run build


FROM node:16

WORKDIR /Fluigi-Cloud

COPY --from=vue-develop-stage /frontend/dist ./dist

# Install dependencies
COPY ./Fluigi-Cloud/package*.json ./

RUN npm install --legacy-peer-deps

COPY ./Fluigi-Cloud/ .

EXPOSE 8080
EXPOSE 3000

CMD [ "npm", "start" ]


