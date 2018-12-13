import random

COMMA=','


def read_data(filename, data_limit=-1):
    raw = []
    data = []
    labels = []
    fin = open(filename)
    skip_first = True
    for line in fin:
        if skip_first:
            skip_first = False
            continue
        line.strip('\n')
        fields = line.split(COMMA)
        for i in range(0, 22):
            fields[i] = float(fields[i])
        raw.append(fields)
    if data_limit > 0:
        raw = random.sample(raw, data_limit)
    for d in raw:
        data.append(d[0:22])
        labels.append(d[22])
    return data, labels
