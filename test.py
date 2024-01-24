import random

a = [i for i in range(45)]

# random.shuffle(a)
b = []

for i in range(5): b.append(a.pop())

print("a = ", a, "\n\nb = ", b)

a += b[::-1]

print ("\n\n\n",a)