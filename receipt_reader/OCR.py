from pathlib import Path
import re
import os
from PIL import Image
import pyocr
import pyocr.builders
import openpyxl as px
import GUI
from WORDs import char_extraction, char_replace, date_pattern, time_pattern
from WORDs import amount_pattern, max_filter, bool_check
""" 指定するエクセルファイルには 「Data」 というシートを作成してください。
"""

def optical_character_recognition(pillow_image):
    """ OCRを実行する。
        入力する画像は pillow で読み込んだものを使用する。
    """

    tools = pyocr.get_available_tools()

    if len(tools) == 0:
        print('Available tool is not found.')
        
    tool = tools[0]

    txt = tool.image_to_string(
        pillow_image,
        lang = 'jpn',
        builder = pyocr.builders.TextBuilder(tesseract_layout=3)
    )
    edit_txt = txt.translate(str.maketrans({',':None, ' ':None, '.':None, '。':None}))
    out_txt = re.sub(r'\\', '¥', edit_txt)
    return out_txt


def image_read(filepath):
    """ ファイルの絶対パスを指定して画像を読み込む。
    """
    return Image.open(filepath)


def resize_image(pillow_image, wid_num, hi_num):
    """ pillowで読み込んだ画像の大きさを変更する。
    """
    mag_list = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]
    
    fx, fy = mag_list[wid_num], mag_list[hi_num]
    size = (round(pillow_image.width * fx), round(pillow_image.height * fy))
    reisized_image = pillow_image.resize(size)

    return reisized_image


def write_data(workbook, sheet_name , dict):
    sheet = workbook[sheet_name]
    maxrow = str(sheet.max_row+1)
    cols = list(map(lambda x:x+maxrow,['A', 'B', 'C']))
    keys = list(dict.keys())
    for key in keys:
        if key == 'date':
            sheet[cols[0]] = dict[key]
        elif key == 'time':
            sheet[cols[1]] = dict[key]
        else:
            sheet[cols[2]] = dict[key]

def loop_to_read(image_path):
        result_dict = {}
        amount_set = set()
        date_flag = True
        time_flag = True
        orig_image = image_read(image_path)
        for h_num in range(3):
            for w_num in range(5):
                resized_image = resize_image(orig_image, w_num, h_num)
                orig_txt = optical_character_recognition(resized_image)

                orig_date = char_extraction(date_pattern(), orig_txt)
                if bool_check(orig_date) and date_flag:
                    date = char_replace(orig_date, ['年', '/'], ['月', '/'], ['日', ''])
                    result_dict['date'] = date
                    date_flag = False

                orig_time = char_extraction(time_pattern(), orig_txt)
                if bool_check(orig_time) and time_flag:
                    time = char_replace(orig_time, ['時', ':'], ['分', ''])
                    result_dict['time'] = time
                    time_flag = False

                amount_out = char_extraction(amount_pattern(), orig_txt)
                if bool_check(amount_out):
                    orig_amount = char_extraction(r'¥[0-9]+', amount_out)
                    amount_no_y = char_replace(orig_amount, ['¥', ''])
                    if amount_no_y not in amount_set:
                        amount_set.add(amount_no_y)
            
            amount = max_filter(amount_set)
        
        result_dict['amount'] = amount

        return result_dict

def main():

    folder_path = Path(GUI.folderopen('読み込むフォルダを選択してください。'))
    work_book_path = GUI.fileopen('エクセルファイルを選択してください。')
    work_book = px.load_workbook(work_book_path)

    image_files = [p for p in folder_path.glob('*') 
    if re.search(r'.*\.(jpeg|jpg|png)$', str(p))]

    for image_path in image_files:
        result_dict = loop_to_read(image_path)

        write_data(work_book, 'Data', result_dict)
        work_book.save(work_book_path)

        # 読み込んだファイルを削除する場合は以下のステップを有効にしてください。
        # os.remove(image_path)

if __name__ == "__main__":
    main()
    GUI.notice_end()