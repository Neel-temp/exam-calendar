import pandas as pd
import calendar

# List of holidays (day, month)
holidays = [
    (1, 1), (26, 1), (17, 3), (7, 4), (15, 8),
    (5, 9), (2, 10), (12, 11), (25, 12), (31, 12)
]

def get_available_days(month, year, day):
    daysavail = []  # Initialize an empty list to store available days
    for day_info in calendar.Calendar().itermonthdays4(year, month):
        # day_info is a tuple (year, month, day, weekday)
        if day_info[3] == 6:  # Skip Sundays
            continue
        if day_info[2] >= day and day_info[1] == month:  # Ensure day is in the correct month
            # Check if the day is a holiday
            if (day_info[2], day_info[1]) not in holidays:
                daysavail.append(day_info)
    return daysavail  # Return the list of available days

def filter_days(daysavail, day):
    filtered_days_list = []
    for days in daysavail:
        if days[2] == day:
            print("Exam day:", days)

        # Add to filtered_days if it's not a Sunday
        if days[3] != 6:  # Ensure it's not a Sunday
            if not filtered_days_list or day[2] != filtered_days_list[-1][2] + 1:
                filtered_days_list.append(days)

    return filtered_days_list


def supply():
    # Read the supply CSV file
    supply_df = pd.read_csv("supply.csv")

    # Initialize a dictionary to hold the subjects
    supply_dict = {}

    # Iterate over each row in the DataFrame
    for index, row in supply_df.iterrows():
        subject = row['Subjects']
        branch = row['branch']

        # Construct the key using the branch name and semester
        key = branch

        # Add the subject to the dictionary under the constructed key
        if key in supply_dict:
            supply_dict[key].append(subject)  # Append to existing list
        else:
            supply_dict[key] = [subject]  # Create a new list with the subject
    return supply_dict

def sem1(subjects_sem1, sem1_final_table, filtered_days):
    # Create a DataFrame to hold the final timetable
    sem1_final_table["Days"] = filtered_days[0:len(subjects_sem1)]  # Add filtered days to the final table
    for branch in subjects_sem1.columns:  # Iterate over column names (branches)
        sample = subjects_sem1[branch].tolist()  # Convert subjects to a list
        sem1_final_table[branch] = sample  # Add branch subjects to the final table

    sup_dic = supply()

    # Integrate supply subjects into the timetable
    for branch_sup, subjects in sup_dic.items():
        if branch_sup in sem1_final_table:
            for subject in subjects:
                if subject in sem1_final_table[branch_sup]:
                    # Remove the subject from its current position
                    sem1_final_table[branch_sup].remove(subject)
                    # Insert the subject at the top of the list
                    sem1_final_table[branch_sup].insert(0, subject)
            #print(f"Moved supply subjects to the top for {branch_sup}: {subjects}")
    print(sem1_final_table)
    # Convert the final table to a DataFrame and save it
    s1 = pd.DataFrame(sem1_final_table)
    s1.to_csv('sem1-finaltimetable.csv', index=False)

def sem2( month , year , day):
    subjects2 = pd.read_csv("sem3-sub.csv")
    row_count2 = len(subjects2)  # Total number of rows in the DataFrame
    print(f"Total number of subjects: {row_count2}")



if __name__ == "__main__":
    print("hello this function file")
