INSERT INTO attempts (is_complete, starting_time, submission_time, created, exercise, section, student)
VALUES
    (1, 1694000000, 1694000200, 1694000250, 'ex', 'sec', 'alice'),
    (1, 1694000000, 1694000200, 1694000250, 'ex', 'sec', 'bob'),
    (1, 1694000000, 1694000200, 1694000250, 'ex', 'sec', 'charlie'),
    (0, 1694000000, NULL, 1694000250, 'ex', 'sec', 'sally'),
    (0, 1694000000, NULL, 1694000250, 'ex', 'sec', 'juliet'),
    (0, 1694000000, NULL, 1694000250, 'ex2', 'sec', 'juliet'),
    (0, 1694000000, NULL, 1694000250, 'ex', 'sec2', 'juliet');
