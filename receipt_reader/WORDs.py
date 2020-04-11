import re

def char_extraction(pattern, text):
    """ 文章中から特定のパターンの文字列を抽出する。
    """
    hit_char = re.search(pattern, text)
    if hit_char != None:
        return hit_char.group()
    else:
        return None

def char_replace(text, *args):
    """ 文章中の指定した文字を置換する。
        リストで、置換前の文字の次に置換後の文字を格納する。
    """
    replace_dict = dict(args)
    return text.translate(str.maketrans(replace_dict))

def date_pattern():
    """ 日付のパターンを返却する。
    """
    return r'[0-9]{4}[年/][0-9]{1,2}[月/][0-9]{1,2}日?'

def time_pattern():
    """ 時間のパターンを返却する。
    """
    return r'[0-9]{1,2}[時:][0-9]{1,2}分?'

def amount_pattern():
    """ 合計金額のパターンを返却する。
    """
    return r'[合代]+.*¥[0-9]+円?'

def max_filter(iter):
    """ リスト、タプル、セットの要素の最大値を返す。
    """
    try:
        max_num = max(iter, key=int)
    except TypeError:
        return None
    except:
        return None
    else:
        return int(max_num)

def bool_check(extract):
    if extract == None:
        return False
    else:
        return True