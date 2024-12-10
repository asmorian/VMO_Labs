import time
import matplotlib.pyplot as plt

uptime = time.monotonic()
print("Time:", uptime)

m = 2 ** 48


def distribution(nums, m):
    intervals_count = 100
    interval_length = m // intervals_count
    intervals = [[] for _ in range(intervals_count)]

    for num in nums:
        for i in range(intervals_count):
            lower_bound = i * interval_length
            upper_bound = (i + 1) * interval_length - 1

            # Если число попадает в текущий интервал, добавляем его
            if lower_bound <= num <= upper_bound:
                intervals[i].append(num)
                break

    freq = []
    for item in intervals:
        freq.append(len(item) / len(nums))

    return freq


def not_rand_rand(num):
    num = str(num).replace('.', '')
    half = len(num) // 2
    not_a = int(num[half:])
    not_b = int(num[:half]) * int(num[half:])
    not_c = int(num)
    return not_a, not_b, not_c


def nod(num1, num2):
    while num2 != 0:
        num1, num2 = num2, num1 % num2
    return num1


def find_a(a):
    while a % 4 != 1:
        a += 1
    return a


def find_b(b, m):
    gcb = 0
    while b <= m:
        gcb = nod(b, m)
        if gcb == 1 and b % 2 == 1:
            break
        else:
            b += 1
    return b


def psd_num(a, b, c, m, length):
    a = find_a(a)
    b = find_b(b, m)
    nums = [((a * c) + b) % m]
    i = 1

    while len(nums) < length:
        nums.append(((a * nums[i - 1]) + b) % m)
        i += 1

    return nums


def create_randoms(len):
    a, b, c, = not_rand_rand(uptime)
    randoms = psd_num(a, b, c, m, len)

    return randoms


def main():
    global nums
    a, b, c, = not_rand_rand(uptime)
    while True:
        length = int(input("Введите кол-во генерируемых числ (0 - выйти) --> "))
        if 20 > length > 0:
            nums = psd_num(a, b, c, m, length)
            print(nums)
        elif length != 0:
            nums = psd_num(a, b, c, m, length)
        else:
            break

    with open('randoms.txt', 'a') as file:
        print("Файл открыт на запись...")
        text = ""
        for i in range(len(nums)):
            if i < len(nums) - 1:
                text += (str(nums[i]))
            else:
                text += str(nums[i])
        file.write(text)
        file.write("\n")
        file.close()
        print("Данные записаны!")

    freq = distribution(nums, m)

    x = list(range(1, 101))
    plt.figure(figsize=(10, 6))
    plt.bar(x, freq)

    plt.xlabel("Values")
    plt.ylabel("Frequency")

    plt.show()


