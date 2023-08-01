
import sys

def main(file_name):
    with open(file_name, 'rb') as f:
        data = list(bytearray(f.read()))

    i = 0
    while i < len(data):
        values = [0]
        j = i
        addr = i
        while j < len(data):
            value = data[j] | (data[j+1] << 8)
            if value > values[-1]:
                j += 2
                values.append(value)
            else:
                j += 1
                break
        if len(values) > 32:
            values.pop(0)
            print('**', 'At ROM', ('$%04x' % addr), '**')
            print(', '.join(['$%04x' % v for v in values]))
            print()
        i = j

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python %s <file_name>" % sys.argv[0])
        sys.exit(1)
    file_name = args.pop(0)
    main(file_name)
