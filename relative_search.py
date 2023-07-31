
import sys

hiragana = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
katakana = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
katakana_voiced = 'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'
hiragana_voiced = 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ'

min_search_len = 3
max_charcode = 0xff

def make_pattern(table, str):
    pattern = [table.index(c) for c in str]
    return pattern

def shift_pattern(pattern, offset):
    pattern = [p + offset for p in pattern]
    return pattern

def search_pattern(data, pattern):
    found = []
    pattern_len = len(pattern)
    for i in range(len(data) - pattern_len):
        for j in range(max_charcode + 1):
            if data[i : i+pattern_len] == shift_pattern(pattern, j):
                found.append((j, i))
    return found

def main(input_file, search_str):
    with open(input_file, 'rb') as f:
        data = list(bytearray(f.read()))
    pattern_table = hiragana
    pattern = make_pattern(pattern_table, search_str)
    results = search_pattern(data, pattern)

    def format(d):
        if d in range(len(pattern_table)):
            return pattern_table[d]
        else:
            return '{%02x}' % d

    for result in results:
        pattern_offset, found_addr = result
        surrounding_data = data[found_addr - 16 : found_addr + 16]
        surrounding_data = [c - pattern_offset for c in surrounding_data]
        surrounding_data = [format(d) for d in surrounding_data]
        surrounding_data = ''.join(surrounding_data)
        print(pattern_offset, hex(found_addr))
        print(surrounding_data)

if __name__ == '__main__':
    args = sys.argv[1:]
    input_file, search_str = args
    if len(search_str) < min_search_len:
        print('Search string must be at least %d characters long.' % min_search_len)
    else:
        main(input_file, search_str)
