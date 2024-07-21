-- Create the database
CREATE DATABASE user_registration;

-- Connect to the database
\c user_registration;

-- Create the Users table
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL
);

-- Create the Profile table
CREATE TABLE Profile (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    profile_picture VARCHAR(255) NOT NULL
);
