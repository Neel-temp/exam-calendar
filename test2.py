import pandas as pd
import calendar
import datetime
from functions import get_available_days, filter_days, sem1,sem2

# Main execution
try:
    emonth = int(input("Enter the month the evaluation is happening (in number): "))
    eyear = int(input("Enter year: "))
    eday = int(input("Day of the exam: "))

    # Validate the input date
    if not (1 <= emonth <= 12):
        raise ValueError("Month must be between 1 and 12.")
    if not (1 <= eday <= 31):
        raise ValueError("Day must be between 1 and 31.")
    if eyear < 1:
        raise ValueError("Year must be a positive integer.")

    # Read the CSV file using pandas
    subjects1 = pd.read_csv("sem1-sub.csv")
    row_count = len(subjects1)  # Total number of rows in the DataFrame
    print(f"Total number of subjects: {row_count}")

    # Get initial available days
    daysavail = get_available_days(emonth, eyear, eday)

    # Adjust for Sunday if the first day available is a Sunday
    if daysavail and daysavail[0][3] == 6:
        print(f"The day entered is a Sunday. \nNew day is: {eday + 1}")
        eday += 1
        daysavail.pop(0)

    # Apply filtering
    filtered_days_list = filter_days(daysavail, eday)

    # Check if we need to generate additional days
    while  row_count < 12:
        nyear = eyear
        nmonth = emonth + 1 if emonth < 12 else 1
        if emonth == 12:
            nyear += 1  # Increment year if December

        nday = 1  # Start from the first day of the next month

        # Check if the first day of the next month is a Sunday
        if datetime.datetime(nyear, nmonth, nday).weekday() == 6:
            nday = 2  # If it's a Sunday, move to the 2nd

        # Additional checks for adjusting nday
        if daysavail and daysavail[-1][2] == 31:
            nday = 2
        elif daysavail and daysavail[-1][2] == 30 and nmonth in [4, 6, 9, 11]:
            nday = 2
        elif daysavail and daysavail[-1][2] == 27 and emonth == 2:
            nday = 2

        # Get new available days for the next month
        new_days = get_available_days(nmonth, nyear, nday)
        daysavail.extend(new_days)  # Append new available days

        # Filter the new available days
        filtered_days_list = filter_days(daysavail, eday)
        # Check again if we have enough filtered days
        if len(filtered_days_list) >= row_count:
            sem1_final_table = {"Days": filtered_days_list[:len(subjects1)]}
            sem1(subjects1, sem1_final_table, filtered_days_list)
            break  # Exit the loop if we have enough days
        else:
            # Increment the day for the next iteration
            nday += 1
            # Optional: Add a limit to avoid infinite loops
            if nday > 31:  # Assuming no month has more than 31 days
                print("Exceeded maximum days in a month without finding enough available days.")
                break
    else:
        print("Still not enough available days after filtering for the next month.")
    print("Filtered days:", daysavail)
    df2=sem2(filtered_days_list)

except ValueError as e:
    print(f"Input error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
