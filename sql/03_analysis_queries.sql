-- 1. KPI principal
SELECT
    COUNT(*) AS total_people,
    ROUND(AVG(annual_income), 2) AS avg_income,
    ROUND(AVG(stress_level), 2) AS avg_stress,
    ROUND(AVG(job_satisfaction), 2) AS avg_satisfaction
FROM immigrant_data;


-- 2. renda média por inglês
SELECT
    english_level,
    ROUND(AVG(annual_income), 2) AS avg_income
FROM immigrant_data
GROUP BY english_level
ORDER BY avg_income DESC;


-- 3. renda média por entrada
SELECT
    entry_type,
    ROUND(AVG(annual_income), 2) AS avg_income
FROM immigrant_data
GROUP BY entry_type
ORDER BY avg_income DESC;


-- 4. renda média por profissão atual
SELECT
    current_profession,
    ROUND(AVG(annual_income), 2) AS avg_income
FROM immigrant_data
GROUP BY current_profession
ORDER BY avg_income DESC;


-- 5. estresse médio por profissão atual
SELECT
    current_profession,
    ROUND(AVG(stress_level), 2) AS avg_stress
FROM immigrant_data
GROUP BY current_profession
ORDER BY avg_stress DESC;


-- 6. satisfação média por profissão atual
SELECT
    current_profession,
    ROUND(AVG(job_satisfaction), 2) AS avg_satisfaction
FROM immigrant_data
GROUP BY current_profession
ORDER BY avg_satisfaction DESC;


-- 7. origem x renda média
SELECT
    country_of_origin,
    ROUND(AVG(annual_income), 2) AS avg_income
FROM immigrant_data
GROUP BY country_of_origin
ORDER BY avg_income DESC;


-- 8. escolaridade x renda média
SELECT
    education_level,
    ROUND(AVG(annual_income), 2) AS avg_income
FROM immigrant_data
GROUP BY education_level
ORDER BY avg_income DESC;


-- 9. transição de carreira
SELECT
    previous_profession,
    current_profession,
    COUNT(*) AS total_people
FROM immigrant_data
GROUP BY previous_profession, current_profession
ORDER BY total_people DESC;


-- 10. horas x estresse
SELECT
    hours_per_week,
    ROUND(AVG(stress_level), 2) AS avg_stress
FROM immigrant_data
GROUP BY hours_per_week
ORDER BY hours_per_week;