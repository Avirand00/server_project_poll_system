DROP TABLE IF EXISTS question;

CREATE TABLE question (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    option_1 VARCHAR(255) NOT NULL,
    option_2 VARCHAR(255) NOT NULL,
    option_3 VARCHAR(255) NOT NULL,
    option_4 VARCHAR(255) NOT NULL
);

INSERT INTO question (title, option_1, option_2, option_3, option_4) VALUES
('What is your favorite programming language?', 'Python', 'Java', 'C++', 'JavaScript'),
('Which type of music do you enjoy the most?', 'Rock', 'Jazz', 'Classical', 'Pop'),
('What is your preferred mode of transportation?', 'Car', 'Bicycle', 'Public Transport', 'Walking'),
('Which season do you like the most?', 'Winter', 'Spring', 'Summer', 'Autumn'),
('What is your favorite type of cuisine?', 'Italian', 'Chinese', 'Mexican', 'Indian');
