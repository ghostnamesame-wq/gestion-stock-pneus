CREATE DATABASE gestion_pneus;

USE gestion_pneus;

CREATE TABLE stock_pneus (

    id INT AUTO_INCREMENT PRIMARY KEY,

    marque VARCHAR(100),

    dimension VARCHAR(50),

    type_pneu VARCHAR(100),

    quantite INT,

    prix DECIMAL(10,2),

    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE mouvements (

    id INT AUTO_INCREMENT PRIMARY KEY,

    action_type VARCHAR(50),

    marque VARCHAR(100),

    dimension VARCHAR(50),

    type_pneu VARCHAR(100),

    quantite INT,

    date_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);