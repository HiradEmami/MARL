import time

t_start = time.time()
for i in range(200000):
    print("hello")
t_end = time.time() - t_start


print("\nTotal runtime:     \t{:.1f}".format(t_end) + " s")