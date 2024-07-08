import glob
import os
import re
from datetime import date

digit_map = {
    "〇": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def chinese_number_to_int(chinese_number: str):
    """将中文数字转换为整数"""
    if not chinese_number:
        return 0

    if chinese_number == "十":
        return 10

    if "十" in chinese_number:
        parts = chinese_number.split("十")
        if parts[0] == "":
            parts[0] = "一"
        if parts[1] == "":
            parts[1] = "零"
        return digit_map.get(parts[0], 0) * 10 + digit_map.get(parts[1], 0)

    result = 0
    for char in chinese_number:
        result = result * 10 + digit_map.get(char, 0)

    return result


def chinese_date_to_date(chinese_date):
    """将中文日期字符串转换为date对象"""
    match = re.search(r"(.*)年(.*)月(.*)日", chinese_date)
    if not match:
        print(chinese_date, "日期格式不正确")
        return None

    chinese_year, chinese_month, chinese_day = match.groups()

    # 替换中文数字为阿拉伯数字
    for chinese_digit, arabic_digit in digit_map.items():
        chinese_year = chinese_year.replace(chinese_digit, str(arabic_digit))

    try:
        year = int(chinese_year)
        month = chinese_number_to_int(chinese_month)
        day = chinese_number_to_int(chinese_day)
        return date(year, month, day)
    except (ValueError, TypeError):
        print(chinese_date, "日期格式不正确")
        return None


def get_all_csv_filepaths(folder_path="./data"):
    """递归获取某文件夹下所有csv文件的路径"""
    return glob.glob(os.path.join(folder_path, "**", "*.csv"), recursive=True)


if __name__ == "__main__":
    pass
