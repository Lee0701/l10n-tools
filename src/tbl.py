
def load_tbl(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = [line.replace('\r', '').replace('\n', '') for line in data]
    data = [line for line in data if len(line) > 0]
    seps = [line.index('=') for line in data]
    data = [(line[:seps[i]], line[seps[i]+1:]) for i, line in enumerate(data)]
    data = [line for line in data if len(line) == 2]
    data = {int(k, 16): v for k, v in data}
    return data
