-- Define the gallery database schema, seed data, and artifact count triggers.
-- create database art_gallery;
--use art_gallery;

-- CREATE TABLE users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100),
--     email VARCHAR(100) UNIQUE,
--     password VARCHAR(100)
-- );

-- CREATE TABLE login (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(100),
--     password VARCHAR(100),
--     role VARCHAR(20)
-- );


-- INSERT INTO login (username, password, role)
-- VALUES ('admin', 'admin123', 'admin');


-- CREATE TABLE tickets (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     V_ID INT,
--     Children INT,
--     Adult INT,
--     SeniorAdult INT,
--     total_amount INT,
--     Date DATE,
--     FOREIGN KEY (V_ID) REFERENCES users(id) ON DELETE CASCADE
-- );



-- CREATE VIEW ticket_summary AS
-- SELECT u.name, t.total_amount, t.Date
-- FROM tickets t
-- JOIN users u ON t.V_ID = u.id;

-- CREATE TABLE visitor (
--     V_ID INT AUTO_INCREMENT PRIMARY KEY,
--     Name VARCHAR(100),
--     Email VARCHAR(100),
--     Contact VARCHAR(20),
--     House_Name VARCHAR(100)
-- );

-- CREATE TABLE employee (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100),
--     designation VARCHAR(100),
--     address VARCHAR(200),
--     phone VARCHAR(15),
--     salary INT,
--     dept VARCHAR(100)
-- );


-- CREATE TABLE artifact (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100),
--     year INT,
--     type VARCHAR(100),
--     dept VARCHAR(100)
-- );

--ALTER TABLE tickets
--ADD CONSTRAINT chk_amount CHECK (total_amount >= 0);

-- CREATE TABLE category (
--     type VARCHAR(50) PRIMARY KEY,
--     artifact_count INT DEFAULT 0
-- );

-- DELIMITER $$

-- CREATE TRIGGER trg_artifact_insert
-- AFTER INSERT ON artifact
-- FOR EACH ROW
-- BEGIN
--     UPDATE category
--     SET artifact_count = artifact_count + 1
--     WHERE type = NEW.Type;

--     IF ROW_COUNT() = 0 THEN
--         INSERT INTO category(type, artifact_count)
--         VALUES (NEW.Type, 1);
--     END IF;
-- END$$

-- DELIMITER ;

-- DELIMITER $$

-- CREATE TRIGGER trg_artifact_delete
-- AFTER DELETE ON artifact
-- FOR EACH ROW
-- BEGIN
--     UPDATE category
--     SET artifact_count = artifact_count - 1
--     WHERE type = OLD.Type;
-- END$$

-- DELIMITER ;

-- DELIMITER $$

-- CREATE TRIGGER trg_artifact_update
-- AFTER UPDATE ON artifact
-- FOR EACH ROW
-- BEGIN
--     IF OLD.Type != NEW.Type THEN

--         UPDATE category
--         SET artifact_count = artifact_count - 1
--         WHERE type = OLD.Type;

--         UPDATE category
--         SET artifact_count = artifact_count + 1
--         WHERE type = NEW.Type;

--         IF ROW_COUNT() = 0 THEN
--             INSERT INTO category(type, artifact_count)
--             VALUES (NEW.Type, 1);
--         END IF;

--     END IF;
-- END$$

-- DELIMITER ;
