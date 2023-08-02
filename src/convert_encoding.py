
import sys

def convert_encoding(input_file, input_encoding, output_file, output_encoding):
    with open(input_file, 'r', encoding=input_encoding) as f:
        data = f.read()
    with open(output_file, 'w', encoding=output_encoding) as f:
        f.write(data)

def main():
    args = sys.argv[1:]
    if len(args) < 4:
        print('Usage: python %s <input_file> <input_encoding> <output_file> <output_encoding>' % sys.argv[0])
        sys.exit(1)
    input_file, input_encoding, output_file, output_encoding = args
    convert_encoding(input_file, input_encoding, output_file, output_encoding)

if __name__ == "__main__":
    main()
