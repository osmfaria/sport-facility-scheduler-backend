[![GitHub package.json version](https://img.shields.io/github/package-json/v/osmfaria/Mshop-backend)](https://img.shields.io/github/package-json/v/osmfaria/Mshop-backend)

## :calendar: Court Scheduler

This is the backend with a RESTful API of an sport-facility/court scheduler. It allows an user  to register their sport facility and add sport courts to it. 
General users can then look for the courts and schedule time slots according to the availability. 



> Link for deployed [API](https://court-scheduler.herokuapp.com/api/) \
> Check the [documentation](https://court-scheduler.herokuapp.com/api/doc/) for proper use

## :toolbox: Tools required

- Docker :whale2:;
- You might also consider using [Postman](https://www.postman.com/downloads/) or [Insomnia](https://insomnia.rest/download) to send API requests.


## 📋 Instalation guide

- Clone this repo;
- On the root folder execute `docker compose up`;
- Once the container is up and running, the configured port is 8000, check it running on `http://localhost:8000/api/doc/`
- Send requests `to http://localhost:8000/api/***` based on the [docs](https://court-scheduler.herokuapp.com/api/doc/).

## 💻 Tech stack

  <img src="https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white" /> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" /> <img src="https://img.shields.io/badge/Prisma-3982CE?style=for-the-badge&logo=Prisma&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" />
  
## ER Diagram

<img src="./diagram-er.png" />

## 🔗 Links

- App frontend [repo](https://github.com/osmfaria/Mshop-frontend);
- Deployed [app](https://mshop-ecommerce.vercel.app/).

## :memo: License

[MIT](./LICENSE)


