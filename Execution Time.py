import numpy as np
import matplotlib.pyplot as plt
import time


def generate_biased_clocks(honest_clocks, f):
    biased_clocks = np.zeros(f)
    sorted_clocks = np.sort(honest_clocks)
    max_value = sorted_clocks[-1]
    for i in range(int(f)):
        biased_clocks[i] = 2 * max_value - honest_clocks[2 * f - i - 1]
    return biased_clocks

def brents_aggregation(honest_clocks, byzantine_clocks, f):
    measurements = np.zeros(3 * f + 1)
    measurements[0:2 * f + 1] = honest_clocks
    measurements[2 * f + 1:] = byzantine_clocks
    scores = np.zeros(3 * f + 1)
    distances = np.zeros(3 * f + 1)
    for i in range(3 * f + 1):
        distances = np.abs(measurements - measurements[i])
        distances.sort()
        scores[i] = np.sum(np.square(distances[1:2 * f + 1]))
    indices = scores.argsort()
    output = np.sum(measurements[indices[0:2 * f]]) / (2 * f)
    return output


def computation_trials(num_trials, f_list):
    biased_clock_brents_output = np.zeros(num_trials)
    result = []
    IoT_result=[0.21630859375, 0.340576171875, 0.466064453125, 0.591552734375, 0.7197265625, 0.854736328125, 0.98828125,
     1.111572265625, 1.24658203125, 1.38330078125, 1.506591796875, 1.656982421875, 1.792236328125, 2.1181640625,
     2.06298828125]
    plt.figure()
    for f in f_list:
        for j in range(num_trials):
            start_time = time.time() * 1000
            honest_clocks = np.random.normal(1.5, 0.3, 2 * f + 1)
            biased_clocks = generate_biased_clocks(honest_clocks, f)

            biased_clock_brents_output[j] = brents_aggregation(honest_clocks, biased_clocks, f)
            end_time = time.time() * 1000
        result.append(end_time - start_time)
    print("Result", result)
    plt.plot(f_list, IoT_result, marker="v", ls="--", label="Rasp Pi")
    plt.plot(f_list, result, marker="^", ls="-", label="PC")
    plt.legend()
    plt.xlabel("Number of f")
    plt.ylabel("Execution Time (ms)")
    plt.xticks(range(1, 16, 2))
    plt.show()


if __name__ == "__main__":
    f_list = range(1, 16, 1)
    requirement = 5
    num_trials = 1000
    computation_trials(num_trials, f_list)
    print("Finished")