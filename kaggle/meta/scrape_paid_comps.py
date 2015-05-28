with open('comps.txt') as f:
    lines = f.readlines()

d = {}
previous2 = ''
previous  = ''

for line in lines:
    if line.startswith('$'):
        key = previous2.replace('\n', '')
        d[key] = [int(x) for x in line[1:].replace(',', '').split()[:2]]
    previous2 = previous
    previous  = line

for k, v in d.items():
    print '%s,%s,%s' % (k, v[0], v[1])
