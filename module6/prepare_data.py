import os
import cPickle as pickle

board_values = []
moves = []
file_names = next(os.walk('./runs'))[2]
for file_name in file_names:
    if file_name.startswith('run_') and file_name.endswith('.pickle'):
        arr = pickle.load(open('./runs/' + file_name, "rb"))  # [board_values, moves]
        board_values.append(arr[0])
        moves.append(arr[1])
        print file_name

pickle.dump([board_values, moves], open("data_bundle.pickle", "wb"))
print 'done'
