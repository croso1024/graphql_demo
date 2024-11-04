## GraphQL Demo Project for Study Group

This is a small project used to demonstrate GraphQL in  company's study group.

### Overview

The project utilizes Hasura's official Docker image, which includes a Hasura GraphQL engine and a PostgreSQL database.

After running, you can access the console through port 8080 to test GraphQL queries & mutations.
The demo database schema and test data can be created using `create_db.sql` and `create_mock_data.sql` in directory.
This is a simple library management database example that demonstrates GraphQL query capabilities.
The ER dirgram below :

<img title="ER-diagram" alt="ER-diagram" src="./Demo_ERD.jpg" width=400>

In addition to the Hasura demo, This demo project also prepared a simple GraphQL backend server implementation using Chalice as the backend framework. This server shares the same PostgreSQL library management example with the Hasura GraphQL server.

### Usage Instructions

1. Hasura Server Setup In the project directory, follow these steps:

Run `docker compose up -d`

This will start a Hasura GraphQL engine accessible at localhost:8000
Also runs PostgreSQL and maps it to port 5433 on the host machine, allowing the locally-running Chalice Server to access PostgreSQL later.


Open your browser and navigate to http://localhost:8080/console to access the Hasura console
In the Console, go to the Data page and switch to the SQL tab

Use `create_db.sql` and `create_mock_data.sql` to create the table and mock data

2. Running the Local Chalice Server

The Chalice server uses the same data source as the above Hasura case , so it's recommended to first run the Hasura example and prepare the test tables and data before trying the Chalice server.
To run the Chalice server:

In your terminal, navigate to the project directory
Run `chalice local` to start the Chalice server on port 8000

Then you can use postman or other api testing tool access the data from `POST /graphql`