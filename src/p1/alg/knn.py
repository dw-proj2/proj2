import math
import multiprocessing
import thread
from time import time

from p1.cate.categories import is_cat
from p1.cate.categories import true_label, false_label
from p1.preprocess.data_split import read_data_float

use_numeric = False
results = []


def knn(train_data, train_labels, test_data, is_cate, weights, k, start, end, pred_labels):
    neighbors = []
    dists = []
    cnt = 0
    for l in range(start, end):
        test_obj = test_data[l]
        for i in range(0, len(train_data)):
            train_obj = train_data[i]
            new_dist = distance(test_obj, train_obj, is_cate, weights)
            if len(neighbors) < k:
                neighbors.append(i)
                dists.append(new_dist)
            else:
                max_neighbor = 0
                for j in range(1, k):
                    if dists[j] < dists[max_neighbor]:
                        max_neighbor = j
                if dists[max_neighbor] > new_dist:
                    dists[max_neighbor] = new_dist
                    neighbors[max_neighbor] = i
        pos_cnt = 0
        for i in range(0, k):
            if train_labels[neighbors[i]] == true_label:
                pos_cnt += 1
        if pos_cnt >= (k + 1) / 2:
            pred_labels[l] = true_label
        else:
            pred_labels[l] = false_label
        neighbors = []
        dists = []
        cnt += 1
        if cnt % 100 == 0:
            print('Thread' + str(thread.get_ident()) + ' ' + str(cnt) + " records processed.")


def distance(d1, d2, is_cate, weights):
    dist = 0.0
    n_attr = len(d1)
    for i in range(0, n_attr):
        if is_cate[i]:
            dist += weights[i] * (1.0 if d1[i] != d2[i] else 0.0)
        else:
            if use_numeric:
                minv = min(d1[i], d2[i])
                maxv = max(d1[i], d2[i])
                if minv != maxv:
                    dist += weights[i] * (1.0 - math.fabs(minv / maxv))
    return dist


def evaluate(pred_labels, true_labels):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(0, len(pred_labels)):
        if pred_labels[i] == true_label:
            if pred_labels[i] == true_labels[i]:
                TP += 1
            else:
                FP += 1
        else:
            if pred_labels[i] == true_labels[i]:
                TN += 1
            else:
                FN += 1
    return TP, FP, TN, FN


def cal_entropies(train_data, train_labels):
    n_data = len(train_data)
    n_attr = len(train_data[0])
    entropies = []
    for i in range(0, n_attr):
        if not is_cat[i]:
            entropies.append(1.0)
        else:
            pos_counter = {}
            neg_counter = {}
            for j in range(0, n_data):
                data = train_data[j]
                if train_labels[j] == true_label:
                    if data[i] not in pos_counter:
                        pos_counter[data[i]] = 1
                    else:
                        pos_counter[data[i]] += 1
                else:
                    if data[i] not in neg_counter:
                        neg_counter[data[i]] = 1
                    else:
                        neg_counter[data[i]] += 1

            entropy = 0.0
            for key in pos_counter:
                pi = pos_counter[key]
                ni = neg_counter[key]
                pp = pi / float(pi + ni)
                pn = ni / float(pi + ni)
                ep = 0 if pp == 0 else pp*math.log(pp)
                en = 0 if pn == 0 else pn*math.log(pn)
                entropy = entropy + (pi + ni) / float(n_data) * (- ep - en)
            entropies.append(entropy)
    return entropies

if __name__ == '__main__':
    train_file = '/Users/koutakashi/codes/dw2/data/full_sample4530_4531.train'
    test_file = '/Users/koutakashi/codes/dw2/data/full_sample110_32017.test'
    train_data, train_labels = read_data_float(train_file)
    test_data, test_labels = read_data_float(test_file)

    # calculate entropy of each attribute
    entropies = cal_entropies(train_data, train_labels)

    k = 1
    use_numeric = False
    num_to_remove = 7
    thread_num = 8

    n_attr = len(train_data[0])
    weights = [1.0] * n_attr

    # # use entropies as weights
    # for i in range(0, n_attr):
    #     weights[i] = 1.0 / entropies[i]

    # remove categorical columns with highest entropy
    entropy_order = []
    for i in range(0, n_attr):
        max_entropy = 0.0
        max_pos = -1
        for j in range(0, n_attr):
            if j in entropy_order:
                continue
            if entropies[j] > max_entropy:
                max_entropy = entropies[j]
                max_pos = j
        entropy_order.append(max_pos)
    # skip non-categorical columns
    num_cate = 0
    for i in range(0, n_attr):
        if entropies[i] == 1.0:
            num_cate += 1
    for i in range(0, num_to_remove):
        weights[entropy_order[num_cate + i]] = 0.0

    start_time = time()
    data_size = len(test_data)
    pred_labels = [None] * data_size
    knn(train_data, train_labels,test_data, is_cat, weights, k, pred_labels)

    elapsed_time = time() - start_time
    print(k, num_to_remove, use_numeric)
    print('Consumed ' + str(elapsed_time) + 's')

    tot = len(test_data)
    TP, FP, TN, FN = evaluate(pred_labels, test_labels)
    print(TP, FP, TN, FN)
    print('precision: ' + str(float(TP + TN) / tot) + ', recall: ' + str(float(TP) / (TP + FN)))