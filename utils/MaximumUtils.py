from Algorithms.pathFinding.Spot import Spot


def second_item(item):
    return item[1]


def max_index(indexed_list: list[tuple[int, int]]):
    return max(indexed_list, key=second_item)[0]


def second_max_index(indexed_list: list[tuple[int, int]]):
    indexed_list.remove(max(indexed_list, key=second_item))
    return max(indexed_list, key=second_item)[0]
