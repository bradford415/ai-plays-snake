import random

test_list = []

test_list.append((5,4,3,2))
test_list.append((1,1,1,1))
test_list.append((3,2,3,2))

memory = random.sample(test_list, 2)

print(memory)