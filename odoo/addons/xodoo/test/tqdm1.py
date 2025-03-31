from tqdm import trange

x = 10000
for i in trange(x):
    for j in range(x):
        k = j * i

print('hello world')