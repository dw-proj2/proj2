import heapq
import math
from time import time

from p2.preprocess.preprocess import read_data

DEBUG = True


def cal_init_dist(data_groups, dist_func, attr_limit, heap):
    cnt = 0
    data_len = len(data_groups)
    for i in range(0, data_len):
        for j in range(i+1, data_len):
            dist = dist_func(data_groups[i], data_groups[j], data, attr_limit)
            g_dist = (dist, i, j)
            heapq.heappush(heap, g_dist)
        cnt += 1
        if cnt % 100 == 0 and DEBUG:
            print('%d init dists generated, heap size: %d' % (cnt, len(heap)))


def h_clustering(data, dist_func, k, attr_limit):
    data_groups = init_group(data)
    removed = [False] * len(data)
    heap = []
    # init distance
    start_time = time()
    cal_init_dist(data_groups, dist_func, attr_limit, heap)
    if DEBUG:
        print('calculate init dists consumed: %fs' % (time() - start_time))

    cnt = 0
    skipped = 0
    while len(data) - cnt > k:
        # find the nearest non-deleted groups
        g_dist = heapq.heappop(heap)
        if removed[g_dist[1]] or removed[g_dist[2]]:
            skipped += 1
            continue
        # combine them into a new group and delete ole groups
        new_group = data_groups[g_dist[1]] + data_groups[g_dist[2]]
        data_groups[g_dist[1]] = None
        data_groups[g_dist[2]] = None
        removed[g_dist[1]] = True
        removed[g_dist[2]] = True
        new_index = len(data_groups)
        # calculate distance between new group and previous non-deleted groups
        for i in range(0, new_index):
            if not removed[i]:
                dist = dist_func(data_groups[i], new_group, data, attr_limit)
                g_dist = (dist, i, new_index)
                heapq.heappush(heap, g_dist)
                removed.append(False)
        data_groups.append(new_group)
        cnt += 1
        if cnt % 100 == 0:
            if DEBUG:
                print('%d new groups generated, heap remaining: %d, skipped: %d' % (cnt, len(heap), skipped))
            if cnt % 1000 == 0:
                heap = re_heap(heap, removed)
    return data_groups


def re_heap(heap, removed):
    new_heap = []
    rm_cnt = 0
    for i in range(0, len(heap)):
        item = heap[i]
        if removed[item[1]] or removed[item[2]]:
            rm_cnt += 1
            continue
        heapq.heappush(new_heap, item)
    if DEBUG:
        print('%d tuples removed' % (rm_cnt))
    return new_heap


def label_groups(groups, data_labels):
    group_labels = []
    for i in range(0, len(groups)):
        group = groups[i]
        counter = {}
        for inst in group:
            label = data_labels[inst][0]
            if label in counter:
                counter[label] += 1
            else:
                counter[label] = 1
        max_cnt = 0
        max_key = None
        for key in counter:
            if counter[key] > max_cnt:
                max_cnt = counter[key]
                max_key = key
        group_labels.append(max_key)
    return group_labels


dist_cache = {}
BIG_FLOAT = 999999999.99


def eucl_pt_distance(i, j, data, attr_limit):
    key = (i, j) if i < j else (j, i)
    if key in dist_cache:
        return dist_cache[key]

    o0 = data[i]
    o1 = data[j]
    dist = _eucl_pt_distance(o0, o1, attr_limit)
    dist_cache[key] = dist
    return dist


def _eucl_pt_distance(o0, o1, attr_limit):
    pow_sum = 0.0
    for i in range(0, attr_limit):
        pow_sum += (o1[i] - o0[i]) * (o1[i] - o0[i])
    return math.pow(pow_sum, 0.5)


def distance_min(g0, g1, data, attr_limit):
    min_dist = BIG_FLOAT
    for i in g0:
        for j in g1:
            new_dist = eucl_pt_distance(i, j, data, attr_limit)
            if new_dist < min_dist:
                min_dist = new_dist
    return min_dist


def distance_max(g0, g1, data, attr_limit):
    max_dist = 0.0
    for i in g0:
        for j in g1:
            new_dist = eucl_pt_distance(i, j, data, attr_limit)
            if new_dist > max_dist:
                max_dist = new_dist
    return max_dist


def distance_avg(g0, g1, data, attr_limit):
    avg0 = group_avg(g0, data)
    avg1 = group_avg(g1, data)
    return _eucl_pt_distance(avg0, avg1, attr_limit)


def init_group(data):
    groups = []
    for d in range(0, len(data)):
        groups.append([d])
    return groups


group_avg_cache = {}


def group_avg(g, data):
    if g in group_avg_cache:
        return group_avg_cache[g]
    avg = _group_avg(g, data)
    group_avg_cache[g] = avg
    return avg


def _group_avg(g, data):
    avg = []
    d = data[g[0]]
    for i in range(0, len(d)):
        avg.append(d[i])
    for i in range(1, len(g)):
        d = data[g[i]]
        for i in range(0, len(d)):
            avg[i] += d[i]
    for i in range(0, len(d)):
        avg[i] /= len(g)
    return avg


def clear_caches():
    global group_avg_cache
    global dist_cache
    group_avg_cache = {}
    dist_cache = {}


def evaluate_pr(groups, true_labels):
    group_sets = []
    for group in groups:
        group_sets.append(set(group))
    data_len = len(true_labels)
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(0, data_len):
        for j in range(i+1, data_len):
            li = true_labels[i][0]
            lj = true_labels[j][0]
            gi = -1
            gj = -1
            for k in range(0, len(group_sets)):
                if i in group_sets[k]:
                    gi = k
                if j in group_sets[k]:
                    gj = k
            if li == lj and gi == gj:
                TP += 1
            elif li != lj and gi == gj:
                FP += 1
            elif li != lj and gi != gj:
                TN += 1
            else:
                FN += 1
    precision = float(TP) / (TP + FP)
    accuracy = float(TP + TN) / (TP + FP + TN + FN)
    recall = 1.0 if TP + FN == 0 else float(TP) / (TP + FN)
    return precision, accuracy, recall


def evaluate_purity(groups, group_labels, true_labels):
    data_len = len(true_labels)
    pos_cnt = 0
    for i in range(0, len(groups)):
        group = groups[i]
        group_label = group_labels[i]
        for data in group:
            if true_labels[data][0] == group_label:
                pos_cnt += 1
    return float(pos_cnt) / data_len


if __name__ == '__main__':
    input = '/Users/koutakashi/codes/dw2/data/Frogs_MFCCs.csv'
    k = 4
    data_limit = -1

    rst_file = open('results2_' + str(time()), 'w+')
    for dist_func in [distance_min, distance_max, distance_avg]:
        for attr_limit in [4, 8, 12, 16, 22]:

            data, labels = read_data(input, data_limit)

            clear_caches()
            groups = h_clustering(data, dist_func, k, attr_limit)
            group_labels = label_groups(groups, labels)
            precision, accuracy, recall = evaluate_pr(groups, labels)
            purity = evaluate_purity(groups, group_labels, labels)
            print('dist: %s, attr_limit: %d' % (str(dist_func), attr_limit))
            print('precision: %f, accuracy: %f, recall: %f, purity: %f\n' % (precision, accuracy, recall, purity))

            rst_file.write('dist: %s, attr_limit: %d\n' % (str(dist_func), attr_limit))
            rst_file.write('precision: %f, accuracy: %f, recall: %f, purity: %f\n' % (precision, accuracy, recall, purity))
    rst_file.close()
