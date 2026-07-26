import threading
import requests
import time

URL = "http://127.0.0.1:8000/api/v1/screener"

times = []


def hit_api():

    start = time.time()

    response = requests.get(URL)

    end = time.time()

    assert response.status_code == 200

    times.append(end - start)


threads = []

overall_start = time.time()

for _ in range(10):

    t = threading.Thread(target=hit_api)

    threads.append(t)

    t.start()

for t in threads:

    t.join()

overall_end = time.time()

print("\n========== PERFORMANCE ==========")

print(f"Total time: {overall_end-overall_start:.2f} sec")

print(f"Average request: {sum(times)/len(times):.2f} sec")

print(f"Fastest: {min(times):.2f} sec")

print(f"Slowest: {max(times):.2f} sec")

assert overall_end-overall_start < 10