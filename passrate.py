with open("du-17-18.csv") as f:
    lines = f.readlines()
    lines = [line.split('\t') for line in lines]
    lines = [[l for l in line if l not in ['',' ']] for line in lines]
    print(lines[0:3])

curr_clg = ''
data = {}
for line in lines:
    line[-1] = line[-1].strip("\n").rstrip("\n")
    if line[-1] in data:
        data[line[-1]][0] +=1
        if line[2] == 'P':
            data[line[-1]][1] += 1
    else:
        data[line[-1]] = [1, 0]
        if line[2] == 'P':
            data[line[-1]][1] += 1

with open('stats_17-18.csv','w') as f:
    for clg in data:
        f.write(f'{clg}\t{data[clg][1]*100/data[clg][0]:.2f}% out of {data[clg][0]}\n\n')

print(data)
