import sys
import matplotlib.pyplot as plt

""" 
zstd -dc pgn_file.zst | python become_master.py
"""

def get_pgns():
    current = []
    for n, line in enumerate(sys.stdin):
        if line.startswith("["):
            first_space = line.find(' ')
            key = line[1:first_space]
            value = line[first_space+1:-2].replace('"', '')
            if key == 'Event':
                if current:
                    yield dict(current)
                current = []
            current.append((key, value))


data = {}
for pgn in get_pgns():
    time_control = pgn['TimeControl']
    if time_control == '600':
        if pgn.get('BlackTitle') == 'FM':
            data[pgn['Black']] = int(pgn['BlackElo'])
        if pgn.get('WhiteTitle') == 'FM':
            data[pgn['White']] = int(pgn['WhiteElo'])

plt.hist(list(data.values()), alpha=0.5, bins=50, label='10+5')
plt.legend(loc='upper right')
plt.show()
