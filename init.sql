CREATE DATABASE IF NOT EXISTS healthcheck;
USE healthcheck;

CREATE TABLE IF NOT EXISTS user (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    url VARCHAR(255),
    response_time FLOAT DEFAULT 0,
    lastcheck DATETIME DEFAULT NULL,
    percantage INT DEFAULT 0,
    status INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS otp (
    email VARCHAR(100) PRIMARY KEY,
    otp INT
);

CREATE TABLE IF NOT EXISTS otplogin (
    email VARCHAR(100) PRIMARY KEY,
    otp INT
);
