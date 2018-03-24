import numpy as np
import random

zero = list("0111010001100011000101110")
zero = map(int, zero)
one = list("0010001100001000010001110")
one = map(int, one)
two = list("0111010010001000100011111")
two = map(int, two)
three = list("0111000001011100000101110")
three = map(int, three)
four = list("0100001000010100111100010")
four = map(int, four)


#=========================================================================================

def resultOfOneExample(inputExample):
    # print "b > {}".format(b)
    v = (-1) * b
    for i in xrange(0, 25):
        v = v + inputExample[i] * weigthW[i]
    # print "v > {}".format(v)
    if v >= 0:
        return 1
    else:
        return 0


#===============================================================================================

# step 1: initialization
alpha = 0.01

inputX = [zero, one, two, three, four]
#print inputX

weigthW = [0] * 25
for i in xrange(0, 25):
    weigthW[i] = random.uniform(-0.999, 0.999)

b = random.uniform(-0.999, 0.999)
epoch = 0

exceptResult = [0, 1, 0, 1, 0]
CORRECT = 0

output = [0] * 5
errors = [1] * 5

print "CORRECT: {}, output: {}, errors: {}".format(CORRECT, output, errors)

while CORRECT!=5:
    CORRECT = 0
    print "epoch : {}".format(epoch)
    print "Start training: "

    for i in xrange(0,5):
        output[i] = resultOfOneExample(inputX[i])
        error = exceptResult[i] - output[i]
        # print "error: {}".format(error)
        for index in xrange(0,25):
            weigthW[index] += alpha * error * inputX[i][index]
        b = b + alpha * error * (-1)
        if exceptResult[i] == output[i]:
            CORRECT += 1;

    epoch +=1
    print "CORRECT: {}, output: {}, target: {}".format(CORRECT, output, exceptResult)
    print "================"
    print ""
    print ""


# Testing the generalisation ability:
print "Testing the generalisation ability:".upper()
for each in inputX:
    for i in xrange(0, 5):
        index = random.randint(0, 24)
        if each[index] == 0:
            each[index] = 1
        elif each[index] == 1:
            each[index] = 0


CORRECT = 0
for i in xrange(0,5):
    output[i] = resultOfOneExample(inputX[i])
    errors[i] = exceptResult[i] - resultOfOneExample(inputX[i])
    # print "error: {}".format(error)
    if resultOfOneExample(inputX[i]) == exceptResult[i]:
        CORRECT += 1
print "CORRECT: {}, output: {}, target: {}, errors: {}".format(CORRECT, output, exceptResult, errors)

	




