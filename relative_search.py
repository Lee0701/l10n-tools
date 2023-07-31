
import sys

hiragana = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
katakana = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
katakana_voiced = 'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'
hiragana_voiced = 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ'

min_search_len = 3
max_charcode = 0xff
surrounding_data_width = 16

def main(input_file, search_str):
    with open(input_file, 'rb') as f:
        data = list(bytearray(f.read()))
    pattern_table = hiragana

    # 檢索할 文字列의 인덱스들을 첫 文字에 對한 差異들의 패턴으로 表現한다.
    offset = -pattern_table.index(search_str[0])
    pattern = [pattern_table.index(c) + offset for c in search_str]
    # 만들어진 패턴으로 檢索을 實行.
    results = search_pattern(data, pattern)

    for result in results:
        result_offset, found_addr = result
        # 찾은 文字列과 周邊 텍스트를 表示할때 使用할 오프셋을 求한다.
        display_offset = result_offset - offset
        surrounding_data = data[found_addr - surrounding_data_width : found_addr + surrounding_data_width]
        surrounding_data = [c + display_offset for c in surrounding_data]
        surrounding_data = [format(pattern_table, d) for d in surrounding_data]
        surrounding_data = ''.join(surrounding_data)
        print(surrounding_data)

def search_pattern(data, pattern):
    found = []
    pattern_len = len(pattern)
    for index in range(len(data) - pattern_len):
        # 檢索할 패턴의 길이만큼 자른다.
        sliced_data = data[index : index+pattern_len]
        offset = -sliced_data[0]
        # 잘라낸 部分을 그 첫 글字에 對한 오프셋들로 變換.
        data_pattern = [d + offset for d in sliced_data]
        # 두 값이 一致하면 檢索結果에 包含.
        if data_pattern == pattern:
            found.append((offset, index))
    return found

def format(pattern_table, d):
    if d in range(len(pattern_table)):
        return pattern_table[d]
    else:
        return '{%02x}' % d

if __name__ == '__main__':
    args = sys.argv[1:]
    input_file, search_str = args
    if len(search_str) < min_search_len:
        print('Search string must be at least %d characters long.' % min_search_len)
    else:
        main(input_file, search_str)
