
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

max_charcode = 0xff

def main(input_file, search_str):
    with open(input_file, 'rb') as f:
        data = list(bytearray(f.read()))
    
    common_results = search_multiple_pattern_tables(search_str, pattern_tables, data)

    for result_addr, result_list in common_results:
        if len(result_list) == 0:
            continue

        raw_text = data[result_addr:result_addr+len(search_str)]
        raw_text = ['$%02x' % c for c in raw_text]
        raw_text = ' '.join(raw_text)

        text = data[result_addr:result_addr+len(search_str)]

        print('**', 'At ROM', '$%04x' % result_addr, '**')
        for result in result_list:
            table_name, display_offset = result
            pattern_table = pattern_tables[table_name]

            sliced_data = data[result_addr:result_addr+len(search_str)]
            sliced_data = [c - display_offset if isinstance(c, int) else c for c in sliced_data]
            text = [pattern_table[c] if isinstance(c, int) and c in range(len(pattern_table)) else text[i] for i, c in enumerate(sliced_data)]

            print('Table', table_name, 'Offset:', '$%02x' % display_offset)

        text = [c if isinstance(c, str) else '{%02x}' % c for c in text]
        text = ''.join(text)
        print('Text:', text)
        print('Raw Text:', raw_text)
        print()

def search_multiple_pattern_tables(search_str, pattern_tables, data):
    results = {}

    for table_name, pattern_table in pattern_tables.items():
        offset, search_results = search_pattern_table(search_str, pattern_table, data)

        if offset is None:
            continue

        for result in search_results:
            result_offset, result_addr = result
            # 찾은 文字列과 周邊 텍스트를 表示할때 使用할 테이블別 오프셋을 求한다.
            display_offset = result_offset - offset
            # 찾아진 住所別로 그룹化
            if result_addr not in results:
                results[result_addr] = []
            results[result_addr].append((table_name, display_offset))

    results = sorted(results.items(), key=lambda x: len(x[1]), reverse=False)
    return results


def search_pattern_table(search_str, pattern_table, data):
    # 檢索할 文字列의 인덱스들을 첫 文字에 對한 差異들의 패턴으로 表現한다.
    # None 값은 Don't care로 處理. 但, 有效한 글字가 두글字 未滿이면 檢索에서 除外한다.
    pattern = [pattern_table.index(c) if c in pattern_table else None for c in search_str]
    filtered = [d for d in pattern if d is not None]
    offset = filtered[0] if len(filtered) > 0 else None
    pattern = [d - offset if d is not None else None for d in pattern]
    if len([c for c in pattern if c is not None]) <= 1:
        pattern = []

    # 만들어진 패턴으로 檢索을 實行한다.
    return offset, search_pattern(data, pattern)

def search_pattern(data, pattern):
    found = []
    pattern_len = len(pattern)
    if pattern.count(None) == pattern_len:
        return found
    first_not_none = [i for i, d in enumerate(pattern) if d is not None][0]
    for index in range(len(data) - pattern_len):
        # 檢索할 패턴의 길이만큼 자른다.
        sliced_data = data[index : index+pattern_len]
        offset = sliced_data[first_not_none]
        # 잘라낸 部分을 그 첫 글字에 對한 오프셋들로 變換.
        data_pattern = [d - offset for d in sliced_data]
        data_pattern = [None if pattern[i] is None else data_pattern[i] for i in range(pattern_len)]
        # 두 값이 一致하면 檢索結果에 包含.
        if data_pattern == pattern:
            found.append((offset, index))
    return found

if __name__ == '__main__':
    args = sys.argv[1:]
    input_file = args.pop(0)
    search_str = ' '.join(args)
    if len([c for c in search_str if c not in hiragana + hiragana_voiced + katakana + katakana_voiced + ' 　']) > 0:
        print('Only large hiragana/katakana/spaces are allowed in search.')
        print('Fullwidth/halfwidth spaces are treated as wildacards.')
        exit()
    main(input_file, search_str)
