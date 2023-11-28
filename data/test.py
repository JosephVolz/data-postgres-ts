import pandas as pd
from datetime import timedelta

# Load data from CSV files
students_df = pd.read_csv('students.csv')
tests_df = pd.read_csv('tests.csv')
submissions_df = pd.read_csv('submissions.csv')
grades_df = pd.read_csv('grades.csv')

# Merge dataframes
submissions_df['submission_time'] = pd.to_datetime(submissions_df['submission_time'])
merged_df = submissions_df.merge(grades_df, on='submission_id', how='left')
last_15_days = merged_df['submission_time'].max() - timedelta(days=15)
recent_submissions = merged_df[merged_df['submission_time'] >= last_15_days]

# 1. Number of unique students submitting at least 1 test each day for the last 15 days
daily_students = recent_submissions.groupby(recent_submissions['submission_time'].dt.date)['student_id'].nunique()

# 2. Number of unique students submitting at least 1 valid test each day for the last 15 days
valid_submissions = recent_submissions[recent_submissions['grade'] > 0]
daily_valid_students = valid_submissions.groupby(valid_submissions['submission_time'].dt.date)['student_id'].nunique()

# 3. Student with the most submissions for each day of the last 15 days
most_submissions = recent_submissions.groupby([recent_submissions['submission_time'].dt.date, 'student_id']).size()
most_submissions_daily = most_submissions.groupby(level=0).idxmax()

# 4. Average grade for each test
# Consider the last valid grade for students who submitted the same test multiple times
last_valid_grades = recent_submissions.sort_values('submission_time').drop_duplicates(['student_id', 'test_id'], keep='last')
average_grade = last_valid_grades.groupby('test_id')['grade'].mean()

print("------------------------------------------")
print("Daily unique students:\n", daily_students)
print("------------------------------------------")
print("Daily unique students with valid tests:\n", daily_valid_students)
print("------------------------------------------")
print("Student with most submissions each day:\n", most_submissions_daily)
print("------------------------------------------")
print("Average grade for each test:\n", average_grade)
print("------------------------------------------")
