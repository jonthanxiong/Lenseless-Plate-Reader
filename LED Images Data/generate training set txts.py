from random import randrange
import os

with open("file_names.txt","r") as f:
    file_names=f.read().split('\n')[:-1]

test_set=set()
test_percentage=.1
test_number = int(len(file_names) * test_percentage)
train_set=set()
train_number=len(file_names)-2*test_number
val_set=set()
val_number=test_number
output_dir="training set texts/"


if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for i in range(test_number):
    test_set.add(file_names.pop(randrange(len(file_names))))

test_set=sorted(list(test_set))
print("test_set:")
print(test_set)

with open(output_dir+"test.txt","w") as f:
    f.write('\n'.join(test_set))

for i in range(val_number):
    val_set.add(file_names.pop(randrange(len(file_names))))

val_set=sorted(list(val_set))
print("val_set:")
print(val_set)

with open(output_dir+"val.txt","w") as f:
    f.write('\n'.join(val_set))

train_set=sorted(file_names)
print("train_set:")
print(train_set)

with open(output_dir+"train.txt",'w') as f:
    f.write('\n'.join(train_set))

trainval_set=train_set.copy()
trainval_set.extend(val_set)
print("trainval_set:")
print(trainval_set)

with open(output_dir+"trainval.txt","w") as f:
    f.write('\n'.join(trainval_set))      
