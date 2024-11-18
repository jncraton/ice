INSERT INTO section (txt_section_name, txt_instructor_name, ts_time_recorded)
VALUES
    ('Intro to Programming', 'Dr. Smith', 1693497600),
    ('Data Science Basics', 'Prof. Johnson', 1694000000),
    ('Algorithms 101', 'Dr. Lee', 1694500000),
    ('Database Systems', 'Dr. Kim', 1695000000),
    ('Web Development', 'Ms. Taylor', 1695500000);

INSERT INTO exercise (fk_section_id, txt_exercise_name, txt_starting_code, txt_desired_output, ts_time_recorded)
VALUES
    (1, 'Intro to Python', 'print("Hello World")', 'Hello World', 1694000000),
    (2, 'Intro to Pandas', 'import pandas as pd', 'DataFrame created', 1694100000),
    (3, 'Binary Search', 'def binary_search(): pass', 'Function implemented', 1694200000),
    (4, 'Intro to SQL', 'SELECT * FROM students;', 'Table displayed', 1694300000),
    (5, 'Web Design Fundamentals', '<html><body>Hello!</body></html>', 'HTML displayed', 1694400000);

INSERT INTO student (txt_student_name, fk_section_id, ts_time_recorded)
VALUES
    ('Alice', 1, 1694500000),
    ('Bob', 2, 1694600000),
    ('Charlie', 3, 1694700000),
    ('David', 4, 1694800000),
    ('Eve', 5, 1694900000);

INSERT INTO student_submission (txt_student_program, txt_student_program_output, bool_is_complete, ts_starting_time, ts_submission_time, ts_time_recorded, fk_exercise_id, fk_student_id)
VALUES
    ('print("Hello")', 'Hello', 1, 1694000000, 1694000200, 1694000250, 1, 1),
    ('pd.DataFrame()', 'DataFrame created', 1, 1694100000, 1694100500, 1694100550, 2, 2),
    ('binary_search([1, 2, 3], 2)', 'Index 1', 1, 1694200000, 1694200800, 1694200850, 3, 3),
    ('SELECT name FROM students;', 'Alice\nBob\n...', 0, 1694300000, NULL, 1694300900, 4, 4),
    ('<h1>Test</h1>', 'Test', 1, 1694400000, 1694401000, 1694401050, 5, 5);
