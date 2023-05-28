# generates preferences for add/drop based on the allocated courses during course allocation 
import csv
import random
import os

def generatePreferences():

    preferences = []
    heading = []
    heading.append("Student Roll Number")
    heading.append("Student First Name")
    heading.append("Student Last Name")
    heading.append("Previously Allocated Course Code")

    path = input("Enter path of the courses DB (0 for default file in same directory): ")
    if int(path) == 0:
        path = "./courses.csv"
    else:
        if not os.path.isfile(path):
            print("no file found")
            return
    
    courses = []
    courseCodes = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            courseCodes.append(int(line["Course Code"]))
            courses.append(line)

    count = len(courseCodes)
    for i in range(1, count):
        heading.append("Preference {}".format(i))
    preferences.append(heading)

    path = input("Enter path of the previously allocated courses DB (0 for default file in same directory): ")
    if int(path) == 0:
        path = "./allocated.csv"
    else:
        if not os.path.isfile(path):
            print("no file found")
            return

    allocated_old = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            allocated_old.append(line)

    countAllocated = len(allocated_old)

    for i in range(0, countAllocated):
        row = []
        row.append(allocated_old[i]["Student Roll Number"])
        row.append(allocated_old[i]["Student First Name"])
        row.append(allocated_old[i]["Student Last Name"])
        row.append(allocated_old[i]["Course Allocated"])

        no_of_preferences = random.randint(0, count - 1)
        random.shuffle(courseCodes)
       
        count_preferences = 0
        for j in range(count):
            if count_preferences == no_of_preferences:
                break

            elif courseCodes[j] != int(allocated_old[i]["Course Allocated"]):
                row.append(courseCodes[j])
                count_preferences += 1
            
        preferences.append(row)

    with open("./preferences_add_drop.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(preferences)


def menu():
    print("Use the following menu:-")
    print("Enter 1 for generating preferences DB")
    print("Enter 0 for exiting code")
    ipt = int(input("Enter your choice: "))
    if ipt == 0:
        exit()
    elif ipt == 1:
        generatePreferences()
    else:
        print("Wrong input, try again")

while True:
    menu()