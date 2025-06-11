# This program creates CSV files that can easily be used to provide land navigation point assignments for ROTC training.
# The program requires a properly formated CSV file, please see the following link:
# https://raw.githubusercontent.com/tsnow2010/ROTC/refs/heads/main/Superlab%20Points%20-%20Sheet1.csv, and will ask for last names of 
# cadets being trained for input.  

import itertools
import random
import csv
import json

# Step 1: Ask for user input.
names = input(
    "Please provide last names of all cadets participating in Land Navigation Training, e.g. 'Snow, Postma, Thompson'"
)
num_train_points = input(
    "How many points will the cadets search for?'"
)
train_name = input(
    "What is the name of the training?"
)

# Creates constants
names = [name.strip() for name in sorted(names.split(','))]
num_cdts = len(names)


# Step 2: Pull land navigation points from CSV file and create dictionary.
points = {}
with open('Superlab Points - Sheet1.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        points[row[2]] = [{'key': row[1]}, {'coordinates': row[0]}]
        
tot_num_points = len(points) # total number of points in CSV file

# Print one element in "points"
#print(points['1'])


# Step 3: Randomize the sets of points that each cadet is given

# Create unique combinations of points into sets
combinations = itertools.combinations(range(1,tot_num_points),int(num_train_points))

# Sets of points that will be distributed to cadets
point_decks = random.sample(sorted(combinations),num_cdts)

# Print "point_decks"
print(point_decks)

# Step 4: Create CSV file with cadet point assignments
with open(f'{train_name} Land Navigation Assignments.csv','w', newline= '') as file:
    writer = csv.writer(file)
    for cdt in range(0,num_cdts):
        point_deck = point_decks[cdt]
        coordinates = []
        for point in point_deck:
            coordinates.append(points[str(point)][1]['coordinates'])
        coordinates.insert(0, f'Cadet {names[cdt]}')
        writer.writerow(coordinates)


# Step 5: Create CSV file with cadet point answer key
with open(f'{train_name} Land Navigation Assignments (Answer Key).csv','w', newline= '') as file:
    writer = csv.writer(file)
    for cdt in range(0,num_cdts):
        point_deck = point_decks[cdt]
        keys = []
        for point in point_deck:
            keys.append(points[str(point)][0]['key'] + f' ({point})')
        keys.insert(0, f'Cadet {names[cdt]}')
        writer.writerow(keys)
