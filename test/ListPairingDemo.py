test_list =  [{'Dune': 8.0}, {'Dunkirk': 1.0}, {'If Beale Street Could Talk': 6.0}, {'The Tragedy of Macbeth': 6.0}, {'Fences': 4.0}]


test_dict = {'Peter Travers': {'Dunkirk': 1.0, 'Belfast': 3.0, 'Carol': 3.0, 'Fences': 4.0, 'If Beale Street Could Talk': 6.0, 'The Tragedy of Macbeth': 6.0, 'Lady Bird': 6.0, 'Sully': 7.0, 'Dune': 8.0, 'Minari': 8.0}, 'Cary Darling': {'Dune': 2.0, 'Dunkirk': 2.0, 'The Tragedy of Macbeth': 4.0, 'Lady Bird': 4.0, 'If Beale Street Could Talk': 7.0, 'Fences': 7.0, 'Belfast': 7.0, 'Carol': 8.0}, 'Adam Patterson': {'Minari': 1.0, 'If Beale Street Could Talk': 2.0, 'Dune': 5.0, 'Dunkirk': 6.0, 'Lady Bird': 7.0}, 'Empire': {'Dune': 1.0, 'Minari': 3.0, 'Dunkirk': 6.0, 'If Beale Street Could Talk': 7.0, 'Lady Bird': 7.0, 'Carol': 10.0}, 'Randy Myers': {'Minari': 3.0, 'Dunkirk': 6.0, 'Dune': 7.0, 'If Beale Street Could Talk': 7.0, 'Lady Bird': 8.0}, 'Total Film': {'Dune': 1.0, 'Dunkirk': 1.0, 'Carol': 7.0, 'Minari': 8.0}, 'Flood Magazine': {'Lady Bird': 2.0, 'Dune': 3.0, 'Minari': 4.0, 'Dunkirk': 6.0}, 'Den of Geek': {'Dune': 1.0, 'Belfast': 2.0, 'Dunkirk': 3.0}, 'Lindsey Bahr': {'Dunkirk': 1.0, 'Lady Bird': 2.0, 'Dune': 3.0, 'Carol': 8.0}, 'Consequence of Sound': {'Dunkirk': 3.0, 'Minari': 3.0, 'If Beale Street Could Talk': 5.0, 'Lady Bird': 5.0}}


list = ["La La Land", "Dunkirk", "Paddington 2", "Lady Bird"]
'''for x in test_dict['Cary Darling']:
    print(x)
    print(test_dict['Cary Darling'])'''

for n in test_dict:
    print('name: {}'.format(n))
    for i in test_dict[n]:
        print('{x}: {y}'.format(x=i, y=test_dict[n][i]))

'''for m in list:
    if m in''' 

print(test_dict.values())