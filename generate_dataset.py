import pandas as pd
import random

countries = ["Brazil", "Mexico", "India", "China", "Colombia", "Philippines"]
entry_types = ["student_visa", "work_visa", "tourist_visa", "marriage", "undocumented"]
previous_jobs = ["engineer", "teacher", "nurse", "police_officer", "driver", "construction_worker", "accountant", "farmer"]
current_jobs = ["construction", "cleaning", "delivery", "office", "IT", "healthcare"]
english_levels = ["basic", "intermediate", "advanced"]
education_levels = ["high_school", "associate", "bachelor", "master"]
employment_types = ["full-time", "part-time", "self-employed"]

data = []

for i in range(1, 301):

    job = random.choice(current_jobs)

    if job == "IT":
        income = random.randint(70000, 130000)
        hours = random.randint(38, 50)
    elif job == "healthcare":
        income = random.randint(60000, 90000)
        hours = random.randint(38, 45)
    elif job == "construction":
        income = random.randint(30000, 60000)
        hours = random.randint(50, 70)
    else:
        income = random.randint(25000, 50000)
        hours = random.randint(40, 60)

    stress = random.randint(4, 10)
    satisfaction = random.randint(3, 9)

    data.append([
        i,
        random.choice(countries),
        random.choice(entry_types),
        random.choice(previous_jobs),
        job,
        random.randint(1, 12),
        random.choice(english_levels),
        random.choice(education_levels),
        hours,
        income,
        stress,
        satisfaction,
        random.choice(employment_types)
    ])

df = pd.DataFrame(data, columns=[
    "person_id","country_of_origin","entry_type","previous_profession",
    "current_profession","years_in_us","english_level","education_level",
    "hours_per_week","annual_income","stress_level","job_satisfaction",
    "employment_type"
])

df.to_csv("data/raw/immigrant_data.csv", index=False)

print("Dataset gerado com sucesso!")