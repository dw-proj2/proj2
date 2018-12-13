COMMA=','


def read_data(filename, data_limit=-1):
    data = []
    labels = []
    fin = open(filename)
    skip_first = True
    cnt = 0
    for line in fin:
        if skip_first:
            skip_first = False
            continue
        line.strip('\n')
        fields = line.split(COMMA)
        for i in range(0, 22):
            fields[i] = float(fields[i])
        data.append(fields[0:22])
        labels.append(fields[22:])
        cnt += 1
        if 0 < data_limit <= cnt:
            break
    return data, labels
