CREATE USER admin WITH PASSWORD 'admin123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON DATABASE auth TO admin;

use auth;

CREATE TABLE users(
    id INT PRIMARY KEY,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)