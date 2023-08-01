
import sys

def main(input_file, input_encoding, output_file, output_encoding):
    with open(input_file, 'r', encoding=input_encoding) as f:
        data = f.read()
    with open(output_file, 'w', encoding=output_encoding) as f:
        f.write(data)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 4:
        print('Usage: python convert_encoding.py <input_file> <input_encoding> <output_file> <output_encoding>')
        sys.exit(1)
    input_file = args.pop(0)
    input_encoding = args.pop(0)
    output_file = args.pop(0)
    output_encoding = args.pop(0)
    main(input_file, input_encoding, output_file, output_encoding)
