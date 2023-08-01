
def load_tbl(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    data = [line.strip() for line in data]
    data = [line for line in data if len(line) > 0]
    data = [line.split('=') for line in data]
    data = [line for line in data if len(line) == 2]
    data = {int(k, 16): v for k, v in data}
    return data
