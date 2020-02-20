import random


def get_random_number(n):
    return random.randint(n - 3, n + 3)


ls = list(map(int, input().split()))

c = 0

for x in ls:
    for i in range(1, x // 2 + 1):
        c += 1
        if random.choice([1, 0]):
            print(i, "+", x - i)
        else:
            print(x - i, "+", i)

while c < 30:
    c += 1
    x = get_random_number((ls[0] + ls[-1]) // 2)
    z = random.randint(1, x - 1)
    print(z, "+", x - z)
