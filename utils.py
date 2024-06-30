import glob
import os
import re


def number_C2E(ChineseNumber):
    """中文数字转整形"""
    map = dict(〇=0, 一=1, 二=2, 三=3, 四=4, 五=5, 六=6, 七=7, 八=8, 九=9, 十=10)
    size = len(ChineseNumber)
    if size == 0:
        return 0
    if size < 2:
        return map[ChineseNumber]

    ans = 0
    continue_flag = False  # 连续进两个的标志位
    for i in range(size):
        if continue_flag:
            continue_flag = False
            continue

        if i + 1 < size and ChineseNumber[i + 1] == "十":
            ans += map[ChineseNumber[i]] * 10
            continue_flag = True
            continue
        ans += map[ChineseNumber[i]]
    return ans


def ChineseDate2EnglishDate(ChineseDate):
    map = dict(〇=0, 一=1, 二=2, 三=3, 四=4, 五=5, 六=6, 七=7, 八=8, 九=9)
    r = re.search(r"(.*)年(.*)月(.*)日", ChineseDate)
    year = r.group(1)
    month = r.group(2)
    day = r.group(3)
    for s, n in map.items():
        year = year.replace(s, str(n))
    month = number_C2E(month)  # 中文转整型
    day = number_C2E(day)

    # 整型转字符串
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)
    return year + "-" + month + "-" + day


def get_all_csv_filepaths(folder_path="./data"):
    return glob.glob(os.path.join(folder_path, "**", "*.csv"), recursive=True)


if __name__ == "__main__":
    pass
