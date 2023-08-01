
import sys

hiragana = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
katakana = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
katakana_voiced = 'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'
hiragana_voiced = 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ'

pattern_tables = {
    'あ': hiragana,
    'が': hiragana_voiced,
    'ア': katakana,
    'ガ': katakana_voiced,
}

min_search_len = 3
max_charcode = 0xff
lookbehind = 4
lookahead = 12

def main(input_file, search_str):
    with open(input_file, 'rb') as f:
        data = list(bytearray(f.read()))
    
    common_results = {}

    for table_name, pattern_table in pattern_tables.items():
        offset, search_results = search_pattern_table(search_str, pattern_table, data)

        if offset is None:
            continue

        for result in search_results:
            result_offset, result_addr = result
            # 찾은 文字列과 周邊 텍스트를 表示할때 使用할 오프셋을 求한다.
            display_offset = result_offset - offset
            if result_addr not in common_results:
                common_results[result_addr] = []
            common_results[result_addr].append((table_name, display_offset))

    for result_addr, result_list in common_results.items():
        if len(result_list) == 0:
            continue

        for result in result_list:
            table_name, display_offset = result
            pattern_table = pattern_tables[table_name]

            surrounding_data = data[result_addr - lookbehind : result_addr + lookahead]
            surrounding_data_raw = ['%02x' % d for d in surrounding_data]
            surrounding_data_raw = ' '.join(surrounding_data_raw)
            surrounding_data = [c + display_offset for c in surrounding_data]
            surrounding_data = [format(pattern_table, d) for d in surrounding_data]
            surrounding_data = ''.join(surrounding_data)

            print('**', 'Table', table_name)
            print('Addr', ':', '$%04x' % result_addr)
            print('Offset', ':', display_offset)
            print('', surrounding_data)
            print('', surrounding_data_raw)
            print()

def search_pattern_table(search_str, pattern_table, data):
    # 檢索할 文字列의 인덱스들을 첫 文字에 對한 差異들의 패턴으로 表現한다.
    # None 값은 Don't care로 處理. 但, 有效한 글字가 두글字 未滿이면 檢索에서 除外한다.
    pattern = [pattern_table.index(c) if c in pattern_table else None for c in search_str]
    filtered = [d for d in pattern if d is not None]
    offset = -filtered[0] if len(filtered) > 0 else None
    pattern = [d + offset if d is not None else None for d in pattern]
    if len([c for c in pattern if c is not None]) <= 1:
        pattern = []

    # 만들어진 패턴으로 檢索을 實行한다.
    return offset, search_pattern(data, pattern)

def search_pattern(data, pattern):
    found = []
    pattern_len = len(pattern)
    if pattern.count(None) == pattern_len:
        return found
    for index in range(len(data) - pattern_len):
        # 檢索할 패턴의 길이만큼 자른다.
        sliced_data = data[index : index+pattern_len]
        offset = -sliced_data[0]
        # 잘라낸 部分을 그 첫 글字에 對한 오프셋들로 變換.
        data_pattern = [d + offset for d in sliced_data]
        pattern_with_dc = [d if d is not None else data_pattern[i] for i, d in enumerate(pattern)]
        # 두 값이 一致하면 檢索結果에 包含.
        if data_pattern == pattern_with_dc:
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
    main(input_file, search_str)
