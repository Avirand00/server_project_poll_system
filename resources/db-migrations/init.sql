DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS user_answer;

CREATE TABLE question (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    option_1 VARCHAR(255) NOT NULL,
    option_2 VARCHAR(255) NOT NULL,
    option_3 VARCHAR(255) NOT NULL,
    option_4 VARCHAR(255) NOT NULL
);

CREATE TABLE user_answer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    answer INT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES question(id)
);

INSERT INTO question (title, option_1, option_2, option_3, option_4) VALUES
('What is your favorite programming language?', 'Python', 'Java', 'C++', 'JavaScript'),
('Which type of music do you enjoy the most?', 'Rock', 'Jazz', 'Classical', 'Pop'),
('What is your preferred mode of transportation?', 'Car', 'Bicycle', 'Public Transport', 'Walking'),
('Which season do you like the most?', 'Winter', 'Spring', 'Summer', 'Autumn'),
('What is your favorite type of cuisine?', 'Italian', 'Chinese', 'Mexican', 'Indian');
