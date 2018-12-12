COMMA=','


def read_data(filename):
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
        data.append(fields[0:22])
        labels.append(fields[22:])
    return data, labels
