#develop stage
FROM node:16 as vue-develop-stage
WORKDIR /frontend
COPY ./Neptune-UI/package*.json ./
RUN yarn install
COPY ./Neptune-UI/ .

RUN yarn build


FROM node:16

WORKDIR /frontend

COPY --from=vue-develop-stage /frontend .

WORKDIR /backend/

# Install dependencies
COPY ./Fluigi-Cloud/package*.json ./

RUN npm ci

COPY ./Fluigi-Cloud/ .

EXPOSE 8080
EXPOSE 3000

CMD [ "npm", "start" ]


