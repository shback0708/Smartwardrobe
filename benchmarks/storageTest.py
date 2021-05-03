from diskcache import Cache
import time
import random
N = 10000

# memory speed benchmark
storage = dict()
start = time.time()
for i in range(N):
    storage[i] = i

sum = 0
for i in range(N):
    sum += storage[random.randrange(0, N)]
    
end = time.time()

mem_time = end - start
print("memory time:", mem_time, sum)

# diskcache speed benchmark
storage = Cache("test")
start = time.time()
for i in range(N):
    storage[i] = i

sum = 0
for i in range(N):
    sum += storage[random.randrange(0, N)]
    
end = time.time()

dc_time = end - start
print("diskcache time:", dc_time, sum)
