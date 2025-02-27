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
    UNIQUE KEY unique_user_question (user_id, question_id),
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
);

INSERT INTO question (title, option_1, option_2, option_3, option_4) VALUES
('What is your favorite programming language?', 'Python', 'Java', 'C++', 'JavaScript'),
('Which type of music do you enjoy the most?', 'Rock', 'Jazz', 'Classical', 'Pop'),
('What is your preferred mode of transportation?', 'Car', 'Bicycle', 'Public Transport', 'Walking'),
('Which season do you like the most?', 'Winter', 'Spring', 'Summer', 'Autumn'),
('What is your favorite type of cuisine?', 'Italian', 'Chinese', 'Mexican', 'Indian');


INSERT INTO user_answer (user_id, question_id, answer) VALUES
(1, 1, 2),
(1, 3, 4),
(1, 5, 1),
(1, 2, 3),
(1, 4, 2),
(3, 2, 1),
(3, 1, 3),
(3, 4, 4),
(3, 3, 2),
(3, 5, 3),
(4, 5, 2),
(4, 3, 1),
(4, 2, 4),
(4, 4, 3),
(4, 1, 2);
