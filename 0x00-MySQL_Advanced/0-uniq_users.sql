-- Creating table users with unique attributes
CREATE TABLE IF NOT EXISTS users(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, email VARCHAR(255) UNIQUE NOT NULL, name VARCHAR(255));
