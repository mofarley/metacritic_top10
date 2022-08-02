list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
count = 0
length = 6
target_list = []
while count < length:
    temp_list = []
    for i in range(1, 3):
        temp_list.append(list[count])
        count += 1
    print(temp_list)
    