import timeit


example_dict = {'Peter Travers': {'Dunkirk': 1.0, 'Belfast': 3.0, 'Carol': 3.0, 'Fences': 4.0, 'If Beale Street Could Talk': 6.0, 'The Tragedy of Macbeth': 6.0, 'Lady Bird': 6.0, 'Sully': 7.0, 'Dune': 8.0, 'Minari': 8.0}, 'Cary Darling': {'Dune': 2.0, 'Dunkirk': 2.0, 'The Tragedy of Macbeth': 4.0, 'Lady Bird': 4.0, 'If Beale Street Could Talk': 7.0, 'Fences': 7.0, 'Belfast': 7.0, 'Carol': 8.0}, 'Adam Patterson': {'Minari': 1.0, 'If Beale Street Could Talk': 2.0, 'Dune': 5.0, 'Dunkirk': 6.0, 'Lady Bird': 7.0}, 'Empire': {'Dune': 1.0, 'Minari': 3.0, 'Dunkirk': 6.0, 'If Beale Street Could Talk': 7.0, 'Lady Bird': 7.0, 'Carol': 10.0}, 'Randy Myers': {'Minari': 3.0, 'Dunkirk': 6.0, 'Dune': 7.0, 'If Beale Street Could Talk': 7.0, 'Lady Bird': 8.0}, 'Total Film': {'Dune': 1.0, 'Dunkirk': 1.0, 'Carol': 7.0, 'Minari': 8.0}, 'Flood Magazine': {'Lady Bird': 2.0, 'Dune': 3.0, 'Minari': 4.0, 'Dunkirk': 6.0}, 'Den of Geek': {'Dune': 1.0, 'Belfast': 2.0, 'Dunkirk': 3.0}, 'Lindsey Bahr': {'Dunkirk': 1.0, 'Lady Bird': 2.0, 'Dune': 3.0, 'Carol': 8.0}, 'Consequence of Sound': {'Dunkirk': 3.0, 'Minari': 3.0, 'If Beale Street Could Talk': 5.0, 'Lady Bird': 5.0}}
'''def conv_to_rank(example_dict):
    for x in example_dict:
        for y in example_dict[x]:
            if example_dict[x][y] == 1:
                example_dict[x][y] = '1st'
            elif example_dict[x][y] == 2:
                example_dict[x][y] = '2nd'
            elif example_dict[x][y] == 3:
                example_dict[x][y] = '3rd'
            else:
                example_dict[x][y] = '{n}th'.format(n=int(example_dict[x][y]))
    return example_dict
start = timeit.default_timer()
test = conv_to_rank(example_dict)
stop = timeit.default_timer()
print('Function Time: ', stop - start)'''

start = timeit.default_timer()
conv_dict = {1:'1st', 2:'2nd', 3:'3rd', 4:'4th', 5:'5th', 6:'6th', 7:'7th', 8:'8th', 9:'9th', 10:'10th'}
for x in example_dict:
    for y in example_dict[x]:
        example_dict[x][y] = conv_dict[example_dict[x][y]]
stop = timeit.default_timer()
#print('Dict Time: ', stop - start)

listy = ['fartman', 'goober ', 'stinker']

for x in listy:
    if x[-1] == ' ':
        continue
    else:
        print(x)