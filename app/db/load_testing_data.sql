INSERT INTO section (section_name, instructor_name, created)
VALUES
    ('CPSC 2020', 'Jon Craton', 1693497600),
    ('Data Science Basics', 'Prof. Johnson', 1694000000),
    ('Algorithms 101', 'Dr. Lee', 1694500000),
    ('Database Systems', 'Dr. Kim', 1695000000),
    ('Web Development', 'Ms. Taylor', 1695500000);

INSERT INTO exercise (section_id, exercise_name, starting_code, desired_output, created)
VALUES
    (1, 'Intro To For Loops', 'for i in range(5):', '0 1 2 3 4', 1694000000),
    (2, 'Intro to Pandas', 'import pandas as pd', 'DataFrame created', 1694100000),
    (3, 'Binary Search', 'def binary_search(): pass', 'Function implemented', 1694200000),
    (4, 'Intro to SQL', 'SELECT * FROM students;', 'Table displayed', 1694300000),
    (5, 'Web Design Fundamentals', '<html><body>Hello!</body></html>', 'HTML displayed', 1694400000);
    

INSERT INTO student (student_name, section_id, created)
VALUES
    ('Alice', 1, 1694500000),
    ('Bob', 2, 1694600000),
    ('Charlie', 3, 1694700000),
    ('David', 4, 1694800000),
    ('Eve', 5, 1694900000);

INSERT INTO student_submission (student_program, student_program_output, is_complete, starting_time, submission_time, created, exercise_id, student_id)
VALUES
    ('for i in range(5):' || char(10) || char(9) || 'print(i)', '0 1 2 3 4', 1, 1694000000, 1694000200, 1694000250, 1, 1),
    ('for i in range(5):' || char(10) || char(9) || 'print(i)', '0 1 2 3 4', 1, 1694000000, 1694000200, 1694000250, 1, 2),
    ('for i in range(5):' || char(10) || char(9) || 'print(i)', '0 1 2 3 4', 1, 1694000000, 1694000200, 1694000250, 1, 3),
    ('for i in range(5):', '', 0, 1694000000, NULL, 1694000250, 1, 4),
    ('for i in range(5):', '', 0, 1694000000, NULL, 1694000250, 1, 5);
    -- ('print("Hello")', 'Hello', 1, 1694000000, 1694000200, 1694000250, 1, 1),
    -- ('pd.DataFrame()', 'DataFrame created', 1, 1694100000, 1694100500, 1694100550, 2, 2),
    -- ('binary_search([1, 2, 3], 2)', 'Index 1', 1, 1694200000, 1694200800, 1694200850, 3, 3),
    -- ('SELECT name FROM students;', 'Alice\nBob\n...', 0, 1694300000, NULL, 1694300900, 4, 4),
    -- ('<h1>Test</h1>', 'Test', 1, 1694400000, 1694401000, 1694401050, 5, 5);

