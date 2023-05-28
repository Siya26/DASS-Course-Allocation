#!/usr/bin/env python3

import csv
import secrets
import names
import pp

students = {}

no_of_students = 200
no_of_courses_for_each_category = 10
total_no_of_courses = 30
maximum_possible_seats_for_each_course = 25
batches = ["2k21", "2k20", "2k22"]
branches = ["CSE", "CSD", "ECE", "ECD", "CLD", "CND", "CHD"]
for i in range(1, no_of_students + 1):
	students[i] = {}
	students[i]["Name"] = names.get_full_name()
	students[i]["Batch"] = secrets.choice(batches)
	students[i]["Branch"] = secrets.choice(branches)

no_of_total_buckets_used = 0
no_of_total_possible_buckets = 6
no_of_buckets_for_each_category = 2
no_of_total_courses_for_each_category = 10
Categories = ["Humanities", "Bouquet", "Open"]

for key in students.keys():
	no_of_buckets_used = 0
	for category in Categories:
		chosen = secrets.randbelow(no_of_buckets_for_each_category + 1)
		while chosen < 1:
			chosen = secrets.randbelow(no_of_buckets_for_each_category)
		for i in range(1, no_of_buckets_for_each_category + 1):
			no_of_buckets_used += 1
			students[key]["Bucket {} Type".format(no_of_buckets_used)] = category
			if chosen > 0:
				no_of_total_buckets_used += 1
				students[key]["Bucket {} ID".format(no_of_buckets_used)] = "id_{}".format(no_of_total_buckets_used)
				chosen -= 1
			else:
				students[key]["Bucket {} ID".format(no_of_buckets_used)] = "None"

Humanities_courses = {
	"Growth and Development" : "Anirban Dasgupta",
	"Internet and Democracy" : "Aakansha Natani",
	"Introduction to Philosophy of Technology" : "Ashwin Jayanti",
	"The Gutenberg Parenthesis" : "Aniket Alam",
	"Migrants and Migrations in Modern South Asia" : "Isha Dubey",
	"Readings in Russian Literature" : "Nazia Akhtar",
	"Science, Technology and Society" : "Radhika Krishnan",
	"Introduction to Film" : "Sushmita Banerjee",
	"Introduction to Existential Philosophy" : "Shipra Dikshit",
	"Comprehension of Indian Music" : "TK Saroja"
}
Bouquet_courses = {
	"Optimisation Methods" : "Naresh Manwani",
	"Advanced Algorithms" : "Suryajith Ch",
	"Principles of Information Security" : "Kannan Srinathan",
	"Data Systems" : "Krishna Reddy P",
	"Software Engineering" : "Karthik Vaidhyanathan",
	"Distributed Systems" : "Lini Thomas",
	"Compilers" : "Venkatesh Choppella",
	"Statistical Methods in AI" : "Vineet Gandhi",
	"Computer Vision" : "Avinash Sharma",
	"Mechatronics System Design" : "Harikumar K"
}
Open_courses = {
	"Introduction to NLP" : "Manish Shrivastava",
	"System and Network Security" : "Ankit Gangwal",
	"Information Security Audit and Assurance" : "Shatrunjay Rawat",
	"Computer Vision" : "Avinash Sharma",
	"Introduction to Game Theory" : "Sujit Gujar",
	"Internals of Application Servers" : "Ramesh Loganathan",
	"Cognitive Science and AI" : "Bapi Raju S",
	"Advanced Optimisation" : "Pawan Kumar",
	"Behavioural Research" : "Vinoo Alluri",
	"Disaster Management" : "Pravin Kumar"
} 
courses = {}
no_of_courses_generated = 0
for category in Categories:
	if category == "Humanities":
		List = list(Humanities_courses.keys())
		Dict = Humanities_courses
	elif category == "Bouquet":
		List = list(Bouquet_courses.keys())
		Dict = Bouquet_courses
	else:
		List = list(Open_courses.keys())
		Dict = Open_courses
	for i in range(1, no_of_courses_for_each_category + 1):
		no_of_courses_generated += 1
		courses[no_of_courses_generated] = {}
		courses[no_of_courses_generated]["Course Type"] = category
		chosen = secrets.randbelow(maximum_possible_seats_for_each_course + 1)
		while chosen < 1:
			chosen = secrets.randbelow(maximum_possible_seats_for_each_course + 1)
		courses[no_of_courses_generated]["No of Seats"] = chosen
		courses[no_of_courses_generated]["Name"] = secrets.choice(List)
		courses[no_of_courses_generated]["Professor's Name"] = Dict[courses[no_of_courses_generated]["Name"]]
		del Dict[courses[no_of_courses_generated]["Name"]]
		List.remove(courses[no_of_courses_generated]["Name"])

for key in students.keys():
	firsts = list(courses.keys())
	for i in range(1, no_of_total_possible_buckets + 1):
		if students[key]["Bucket {} ID".format(i)] != "None":
			for category in Categories:
				if category == students[key]["Bucket {} Type".format(i)]:
					count = secrets.randbelow(no_of_total_courses_for_each_category + 1)
					while count < 1:
						count = secrets.randbelow(no_of_total_courses_for_each_category + 1)
					temp = []
					for course in courses.keys():
						if courses[course]["Course Type"] == category:
							temp.append(course)
					students[key]["Bucket {} Preferences".format(i)] = []
					while count > 0:
						temp_var = secrets.choice(temp)
						if len(students[key]["Bucket {} Preferences".format(i)]) == 0:
							while temp_var not in firsts:
								temp.remove(temp_var)
								temp_var = secrets.choice(temp)
						students[key]["Bucket {} Preferences".format(i)].append(temp_var)
						temp.remove(temp_var)
						count -= 1
						
with open("courses.csv", "w") as file:
	row_writer = csv.writer(file)
	row_writer.writerow(["Course ID", "Name", "No of Seats", "Professor's Name", "Course Type"])
	for course in courses.keys():
		row_writer.writerow([course, courses[course]["Name"], courses[course]["No of Seats"], courses[course]["Professor's Name"], courses[course]["Course Type"]])

with open("student_details.csv", "w") as file:
	row_writer = csv.writer(file)
	row_writer.writerow(["Name", "Roll Number", "Branch", "Batch"])
	for student in students.keys():
		row_writer.writerow([students[student]["Name"], student, students[student]["Branch"], students[student]["Batch"]])

with open("student_buckets.csv", "w") as file:
	row_writer = csv.writer(file)
	temp = ["Roll Number"]
	for i in range(1, no_of_total_possible_buckets + 1):
		temp.append("Bucket {} ID".format(i))
	row_writer.writerow(temp)
	for student in students.keys():
		temp = [student]
		for i in range(1, no_of_total_possible_buckets + 1):
			temp.append(students[student]["Bucket {} ID".format(i)])
		row_writer.writerow(temp)
		
with open("buckets.csv", "w") as file:
	row_writer = csv.writer(file)
	temp = ["Bucket ID", "Bucket Type"]
	for i in range(1, no_of_total_courses_for_each_category + 1):
		temp.append("Preference {}".format(i))
	row_writer.writerow(temp)
	for student in students.keys():
		for bucket in range(1, no_of_total_possible_buckets + 1):
			temp = []
			if students[student]["Bucket {} ID".format(bucket)] != "None":
				temp.append(students[student]["Bucket {} ID".format(bucket)])
				temp.append(students[student]["Bucket {} Type".format(bucket)])
				temp.extend(students[student]["Bucket {} Preferences".format(bucket)])
			while len(temp) != no_of_total_courses_for_each_category + 2:
				temp.append("None")
			row_writer.writerow(temp)
				