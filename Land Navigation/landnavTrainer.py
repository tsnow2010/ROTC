# This program creates one MS Excel workbook that can easily be used to provide land navigation point assignments for ROTC training.
# Requires properly formated CSV files.  
# Please see the repository for examples.

# By Tyler Snow

import itertools
import random
import csv
import json
import pandas as pd
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side
import os

# Set paths for changing directories
home_path = os.getcwd()
assignments_path = f"{home_path}/'Assignments'"


# Generates assignment list and corresponding answer key in .csv format.
def generate_assignments(group:str, num_cdts:int, num_train_points:int):
    
    # Constants
    group = group # Group name
    num_cdts = num_cdts # Number of cadets in group
    num_train_points = num_train_points # Number of points trainees are looking for
    
    # Step 1: Pull land navigation points from CSV file and create dictionary.
    points = {}
    with open(f'{home_path}/LN_Points.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            points[row[2]] = [{'key': row[1]}, {'coordinates': row[0]}]
            
    tot_num_points = len(points) # total number of points in CSV file
    
    # Step 2: Randomize the sets of points that each cadet is given
    # Create unique combinations of points into sets
    combinations = itertools.combinations(range(1,tot_num_points),int(num_train_points))
    
    # Sets of points that will be distributed to cadets
    point_decks = random.sample(sorted(combinations),num_cdts)
    
    # Step 3: Create CSV file with cadet point assignments
    with open(f'{group} Assignments.csv','w', newline= '') as file:
        writer = csv.writer(file)
        for i in range(0,num_cdts):
            point_deck = point_decks[i]
            coordinates = []
            for point in point_deck:
                coordinates.append(points[str(point)][1]['coordinates'])
            coordinates.insert(0, f'Cadet {i+1}')
            writer.writerow(coordinates)
            writer.writerow(['Answer']) # Add line for writing answers   + ','*(num_train_points-1)]
    
    # Step 4: Create CSV file with cadet point answer key
    with open(f'{group} (Answer Key).csv','w', newline= '') as file:
        writer = csv.writer(file)
        for i in range(0,num_cdts):
            point_deck = point_decks[i]
            keys = []
            for point in point_deck:
                keys.append(points[str(point)][0]['key'] + f' ({point})')
            keys.insert(0, f'Cadet {i+1}')
            writer.writerow(keys)   
