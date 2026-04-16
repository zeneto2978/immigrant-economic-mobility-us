CREATE TABLE immigrant_data (
    person_id INTEGER PRIMARY KEY,
    country_of_origin VARCHAR(100),
    entry_type VARCHAR(50),
    previous_profession VARCHAR(100),
    current_profession VARCHAR(100),
    years_in_us INTEGER,
    english_level VARCHAR(30),
    education_level VARCHAR(30),
    hours_per_week INTEGER,
    annual_income NUMERIC(12,2),
    stress_level INTEGER,
    job_satisfaction INTEGER,
    employment_type VARCHAR(30)
);