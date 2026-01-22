# This simple script can assist in creating sight picture targets for PMI instruction.

RANGES_M = [100,150,200,250,300] # ranges for Tables V,VI in BRM

ACTUAL_H = 40 # inches tall of B Target
VIEWING_D = 60 # inches away from sheet of paper
M_TO_IN_RATE = 39.3701

print(f'This exercise and the below table assumes that the Soldier is {VIEWING_D}" away from the paper:')

for range in RANGES_M:
    range_in = range * M_TO_IN_RATE
    angular_size = ACTUAL_H/range_in
    perceived_h = angular_size*VIEWING_D # formula for angular size x viewing distance
    #print(f"Angular size is {angular_size}.")
    print(f'--\nAt {range}m, the target appears to be {perceived_h: .2f}" tall.')
