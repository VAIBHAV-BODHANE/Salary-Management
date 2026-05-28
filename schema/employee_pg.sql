CREATE TABLE IF NOT EXISTS employees (
    empid     SERIAL PRIMARY KEY,
    full_name TEXT   NOT NULL,
    job_title TEXT   NOT NULL,
    country   TEXT   NOT NULL,
    salary    REAL   NOT NULL,
    doj       TEXT   NOT NULL,
    dob       TEXT   NOT NULL
);
