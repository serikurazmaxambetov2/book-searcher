FROM node:22.11.0

# Установка зависимостей
WORKDIR /backend
COPY yarn.lock package.json ./
RUN yarn install

# Билдим
COPY . .
RUN yarn build

# Запуск
CMD sleep 10 && yarn prisma db push && yarn start:prod
