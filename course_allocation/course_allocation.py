#!/usr/bin/env python3

import csv
import pp
import secrets

no_of_total_possible_buckets = 6
no_of_buckets_for_each_category = 2
no_of_total_courses_for_each_category = 10
Categories = ["Humanities", "Bouquet", "Open"]

Student = {}
with open("student_details.csv", "r") as file:
	reader = csv.DictReader(file)
	for row in reader:
		Student[int(row["Roll Number"])] = {}
		Student[int(row["Roll Number"])]["Name"] = row["Name"]
		Student[int(row["Roll Number"])]["Branch"] = row["Branch"]
		Student[int(row["Roll Number"])]["Batch"] = row["Batch"]

with open("student_buckets.csv", "r") as file:
	reader = csv.DictReader(file)
	for row in reader:
		for bucket in range(1, no_of_total_possible_buckets + 1):
			Student[int(row["Roll Number"])]["Bucket {} ID".format(bucket)] = row["Bucket {} ID".format(bucket)]
			Student[int(row["Roll Number"])]["Bucket {} Preferences".format(bucket)] = []

with open("buckets.csv", "r") as file:
	reader = csv.DictReader(file)
	for row in reader:
		for key in Student.keys():
			for bucket in range(1, no_of_total_possible_buckets + 1):
				if Student[key]["Bucket {} ID".format(bucket)] == row["Bucket ID"]:
					temp = []
					for i in range(1, no_of_total_courses_for_each_category + 1):
						if row["Preference {}".format(i)] == "None":
							break
						temp.append(row["Preference {}".format(i)])
					Student[key]["Bucket {} Preferences".format(bucket)] = temp
					Student[key]["Bucket {} Type".format(bucket)] = row["Bucket Type"]
					break
#print("Students dictionary:")
#pp(Student, sort_dicts=True)
#
#print()
#print()

Course = {}
with open("courses.csv","r") as file:
	reader = csv.DictReader(file)
	for row in reader:
		Course[row["Course ID"]] = {}
		Course[row["Course ID"]]["Name"] = row["Name"]
		Course[row["Course ID"]]["No of Seats"] = int(row["No of Seats"])
		Course[row["Course ID"]]["Professor's Name"] = row["Professor's Name"]
		Course[row["Course ID"]]["No of Seats Available"] = int(row["No of Seats"])
		Course[row["Course ID"]]["Course Type"] = row["Course Type"]
#print("Courses dictionary:")
#pp(Course, sort_dicts=True)
#
#print()
#print()

Extracted_preferences = {}
for category in Categories:
	Extracted_preferences[category] = {}
	for course in Course.keys():
		if Course[course]["Course Type"] != category:
			continue
		Extracted_preferences[category][course] = {}
		for i in range(1, no_of_total_courses_for_each_category + 1):
			Extracted_preferences[category][course]["Student List for Preference {}".format(i)] = []

for student in Student.keys():
	for bucket in range(1, no_of_total_possible_buckets + 1):
		for i in range(len(Student[student]["Bucket {} Preferences".format(bucket)])):
			if Student[student]["Bucket {} ID".format(bucket)] != 'None':
				Extracted_preferences[Student[student]["Bucket {} Type".format(bucket)]][Student[student]["Bucket {} Preferences".format(bucket)][i]]["Student List for Preference {}".format(i+1)].append(Student[student]["Bucket {} ID".format(bucket)])
#print("Extracted Preferences:")
#pp(Extracted_preferences, sort_dicts=True)
#
#print()
#print()

for category in Categories:
	for i in range(1, no_of_total_courses_for_each_category + 1):
		for course in Extracted_preferences[category].keys():
			allocated = []
			if len(Extracted_preferences[category][course]["Student List for Preference {}".format(i)]) < Course[course]["No of Seats Available"]:
				allocated.extend(Extracted_preferences[category][course]["Student List for Preference {}".format(i)])
				Course[course]["No of Seats Available"] -= len(Extracted_preferences[category][course]["Student List for Preference {}".format(i)])
			elif len(Extracted_preferences[category][course]["Student List for Preference {}".format(i)]) == Course[course]["No of Seats Available"]:
				allocated.extend(Extracted_preferences[category][course]["Student List for Preference {}".format(i)])
				Course[course]["No of Seats Available"] -= len(Extracted_preferences[category][course]["Student List for Preference {}".format(i)])
			else:
				temp = Extracted_preferences[category][course]["Student List for Preference {}".format(i)]
				count = 0
				while len(temp) > 0 and count < Course[course]["No of Seats"]:
					chosen = secrets.choice(temp)
					temp.remove(chosen)
					allocated.append(chosen)
					count += 1
				Course[course]["No of Seats Available"] = 0
			for value in allocated:
				for course2 in Extracted_preferences[category].keys():
					for j in range(1, no_of_total_courses_for_each_category + 1):
						if value in Extracted_preferences[category][course2]["Student List for Preference {}".format(j)]:
							Extracted_preferences[category][course2]["Student List for Preference {}".format(j)].remove(value)
				for student in Student.keys():
					for bucket in range(1, no_of_total_possible_buckets + 1):
						if value == Student[student]["Bucket {} ID".format(bucket)]:
							Student[student]["Course {} Allocated".format(bucket)] = course
						else:
							continue

#print("Extracted Preferences:")
#pp(Extracted_preferences, sort_dicts=True)
#
#print()
#print()

width = 120
with open("output.txt", "w") as file:
	for student in Student:
		file.write("{} :\n".format(student))
		for key in sorted(Student[student].keys()):
			file.write("{: <14s}{} : {}\n".format(" ",key, Student[student][key]))
		file.write("-"*width)
		file.write("\n")
#width = 120
#for student in Student:
#	print("{} :".format(student))
#	for key in sorted(Student[student].keys()):
#		print("{: <14s}{} : {}".format(" ",key, Student[student][key]))
#	print("-"*width)