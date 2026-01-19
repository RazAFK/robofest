with open('additions/Tests/testms_into_sm.txt', 'r') as file:
    lines = []
    for line in file:
        lines.append(line)

    data = []
    for line in lines[2:]:
        data.append(float(line.split()[-1]))
    print(sum(data)/len(data))
    k = round(500/37.85, 3)
    print(k)
    print(5*k)
