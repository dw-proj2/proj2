from p1.cate.categories import jobs, maritals, educations, nyu, contacts, months, weekday, poutcomes, labels

SEP = ';'


def preprocess(input, output):
    fin = open(input)
    fout = open(output, 'w+')
    skip_first = True
    for line in fin:
        if skip_first:
            skip_first = False
            continue
        line = line.strip('\r\n')
        fields = str.split(line, SEP)
        # age
        # job
        fields[1] = jobs[fields[1]]
        # marital
        fields[2] = maritals[fields[2]]
        # education
        fields[3] = educations[fields[3]]
        # default, housing, loan
        fields[4] = nyu[fields[4]]
        fields[5] = nyu[fields[5]]
        fields[6] = nyu[fields[6]]
        # contact
        fields[7] = contacts[fields[7]]
        # month
        fields[8] = months[fields[8]]
        # day of weeks
        fields[9] = weekday[fields[9]]
        # duration (dropped)
        fields.remove(fields[10])
        # campaign, pdays, previous
        # poutcome
        fields[13] = poutcomes[fields[13]]
        # emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed
        # label
        fields[19] = labels[fields[19]]
        fout.write(SEP.join(fields))
        fout.write('\n')
    fin.close()
    fout.close()


if __name__ == '__main__':
    input = '/Users/koutakashi/codes/dw2/data/bank-additional-full.csv'
    output = input + '_preprocessed'
    preprocess(input, output)