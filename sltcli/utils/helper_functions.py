banner_text = """
 _______  _    _________                _______  _______        _______  _       _________
(  ____ \( \   \__   __/      |\     /|(  ___  )(  ____ \      (  ____ \( \      \__   __/
| (    \/| (      ) (         | )   ( || (   ) || (    \/      | (    \/| (         ) (   
| (_____ | |      | |         | |   | || (___) || (_____       | |      | |         | |   
(_____  )| |      | |         ( (   ) )|  ___  |(_____  )      | |      | |         | |   
      ) || |      | |          \ \_/ / | (   ) |      ) |      | |      | |         | |   
/\____) || (____/\| |           \   /  | )   ( |/\____) |      | (____/\| (____/\___) (___
\_______)(_______/)_(            \_/   |/     \|\_______)      (_______/(_______/\_______/
"""
seperator_print = "=" * 92
banner = '\n'.join([seperator_print, banner_text, seperator_print])


def add_values_by_matching_key(dictionary, match_str):
    total = 0
    match_str = match_str.lower()
    for key, value in dictionary.items():
        if match_str in key.lower():
            total += value
    return total


def daily_consolidate(dictionary, keywords_array):
    data = [[keyword, 0] for keyword in keywords_array]
    for dataKey in data:
        dataKey[1] = add_values_by_matching_key(dictionary, dataKey[0])
    return data
