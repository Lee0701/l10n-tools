
import sys

from tbl import load_tbl

line_len = 16

def dump_with_tbl(tbl_file, input_file):
    with open(input_file, 'rb') as f:
        data = list(bytearray(f.read()))
    tbl = load_tbl(tbl_file)

    lines = []
    for i, b in enumerate(data):
        if i % line_len == 0:
            addr = '$' + ('%04x' % i).ljust(8, ' ')
            lines.append((addr, [], []))
        lines[-1][1].append('%02x' % b)

    i = 0
    while i < len(data):
        line = lines[i // line_len][2]
        for k in range(8, 0, -1):
            b = int.from_bytes(bytearray(data[i:i+k]))
            if b in tbl:
                line.append(tbl[b])
                i += k
                break
        else:
            b = data[i]
            line.append(f'<{b:02x}>')
            i += 1

    lines = [addr + ' '.join(v) + '  ' + ''.join(c) for addr, v, c in lines]
    result = '\n'.join(lines) + '\n'
    return result

def main():
    args = sys.argv[1:]
    if len(args) != 3:
        print("Usage: python %s <tbl_file> <input_file> <output_file>" % sys.argv[0])
        sys.exit(1)
    tbl_file, input_file, output_file = args
    result = dump_with_tbl(tbl_file, input_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

if __name__ == "__main__":
    main()
