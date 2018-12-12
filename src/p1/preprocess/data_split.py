import random

from p1.cate.categories import true_label, is_cat
from preprocess import SEP


def read_data(filename):
    f = open(filename)
    data = []
    labels = []
    for line in f:
        line = line.strip('\n')
        fields = line.split(SEP)
        data.append(fields[:len(fields)-1])
        labels.append(fields[len(fields)-1])
    return data, labels


def read_data_float(filename):
    f = open(filename)
    data = []
    labels = []
    for line in f:
        line = line.strip('\n')
        fields = line.split(SEP)
        for i in range(0, len(fields)-1):
            if not is_cat[i]:
                fields[i] = float(fields[i])
        data.append(fields[:len(fields)-1])
        labels.append(fields[len(fields)-1])
    return data, labels


def data_split(data, labels, train_ratio, pos_ratio, filename):
    pos_data = []
    neg_data = []
    for i in range(0, len(data)):
        if labels[i] == true_label:
            pos_data.append(i)
        else:
            neg_data.append(i)
    print('Positive data: ', len(pos_data), 'Negative samples: ', len(neg_data))

    sample_num = int(len(data) * train_ratio)
    pos_sample_num = int(sample_num * pos_ratio)
    if pos_sample_num > len(pos_data):
        pos_sample_num = len(pos_data)
    neg_sample_num = sample_num - pos_sample_num
    if neg_sample_num > len(neg_data):
        neg_sample_num = len(neg_data)
        pos_sample_num = sample_num - neg_sample_num
    print('Positive samples: ', pos_sample_num, 'Negative samples: ', neg_sample_num)

    pos_samples = random.sample(pos_data, pos_sample_num)
    neg_samples = random.sample(neg_data, neg_sample_num)

    train_file = open(filename + str(pos_sample_num) + '_' + str(neg_sample_num) + '.train' , 'w+')
    test_file = open(filename + str(len(pos_data) - pos_sample_num) + '_' + str(len(neg_data) - neg_sample_num) + '.test', 'w+')

    for i in range(0, len(data)):
        if i in pos_samples or i in neg_samples:
            train_file.write(SEP.join(data[i]) + SEP + labels[i])
            train_file.write('\n')
        else:
            test_file.write(SEP.join(data[i]) + SEP + labels[i])
            test_file.write('\n')
    train_file.close()
    test_file.close()


if __name__ == '__main__':
    input = '/Users/koutakashi/codes/dw2/data/bank-additional-full.csv_preprocessed'
    output = '/Users/koutakashi/codes/dw2/data/full_sample'
    data, labels = read_data(input)
    train_ratio = 0.22
    pos_ratio = 0.5
    data_split(data, labels, train_ratio, pos_ratio, output)
