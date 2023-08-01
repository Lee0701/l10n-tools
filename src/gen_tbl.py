
import sys

from consts import pattern_tables

def main(gen_params, out_file):
    result = []
    for table_id, offset in gen_params.items():
        pattern_table = pattern_tables[table_id]
        for i, c in enumerate(pattern_table):
            result.append('%02x=%s' % (i + offset, c))
    result = '\n'.join(result)
    with open(out_file, 'w') as f:
        f.write(result)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 2:
        print('Usage: python %s <params> <out_file>' % sys.argv[0])
        exit(1)
    params = args.pop(0)
    params = [item.strip().split('=') for item in params.split(',')]
    params = {k: int(v, 16) for k, v in params}
    out_file = args.pop(0)
    main(params, out_file)
