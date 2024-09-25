class Item:
    def __init__(self, profit, weight, num):
        self.profit = profit
        self.weight = weight
        self.num = num


def fractional_knapsack(w, arr):

    arr.sort(key=lambda x: (x.profit / x.weight), reverse=True)
    item_list = []
    finalvalue = 0.0

    for item in arr:

        if item.weight <= w:
            w -= item.weight
            finalvalue += item.profit
            item_list.append(item.num)

        else:
            finalvalue += item.profit * w / item.weight
            item_list.append([item.num, w])
            break

    return finalvalue, item_list


def knapsack(wt, val, w, n, t):
    if n == 0 or w == 0:
        return 0, []

    if t[n][w] != -1:
        return t[n][w]

    if wt[n - 1] <= w:
        include_item_value, include_items = knapsack(
            wt, val, w - wt[n - 1], n - 1, t)
        exclude_item_value, exclude_items = knapsack(wt, val, w, n - 1, t)

        if val[n - 1] + include_item_value > exclude_item_value:
            t[n][w] = val[n - 1] + include_item_value, include_items + [n - 1]
        else:
            t[n][w] = exclude_item_value, exclude_items

        return t[n][w]

    elif wt[n - 1] > w:
        t[n][w] = knapsack(wt, val, w, n - 1, t)
        return t[n][w]
