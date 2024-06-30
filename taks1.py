from typing import Generator

import pandas as pd
from rich.progress import Progress

from utils import ChineseDate2EnglishDate, get_all_csv_filepaths


def get_chunks(file_path: str, chunk_size: int) -> Generator[pd.DataFrame, None, None]:
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    for chunk in chunks:
        yield chunk


def process_file(file_path: str, chunk_size: int, progress: Progress) -> pd.DataFrame:
    chunks = get_chunks(file_path, chunk_size)
    filtered_df = pd.DataFrame()

    task = progress.add_task(
        "[cyan]Processing file...", total=pd.read_csv(file_path).shape[0] / chunk_size
    )

    for chunk in chunks:
        filtered_chunk = chunk[chunk["案件类型"].isin(["刑事案件", "民事案件"])]
        filtered_chunk = filtered_chunk[filtered_chunk["审理程序"].notnull()]
        filtered_chunk = filtered_chunk[filtered_chunk["审理程序"].str.contains("一审")]
        filtered_chunk = filtered_chunk[filtered_chunk["文书内容"].notnull()]
        filtered_chunk["审判法院所在地址"] = filtered_chunk["文书内容"].str.extract(
            r"(.+?)人民法院"
        )
        filtered_chunk["判决时间"] = filtered_chunk["文书内容"].str.extract(
            r"(二〇[一二三四五六七八九十〇]{2}年[一二三四五六七八九十〇]{1,2}月[一二三四五六七八九十〇]{1,3}日)"
        )
        filtered_chunk = filtered_chunk[filtered_chunk["判决时间"].notnull()]
        filtered_chunk["判决时间"] = filtered_chunk["判决时间"].apply(
            ChineseDate2EnglishDate
        )
        filtered_chunk["判决时间"] = pd.to_datetime(
            filtered_chunk["判决时间"], format="%Y-%m-%d", errors="coerce"
        )
        filtered_chunk = filtered_chunk[filtered_chunk["判决时间"].notnull()]

        filtered_df = pd.concat([filtered_df, filtered_chunk], ignore_index=True)

        progress.advance(task)

    return filtered_df


if __name__ == "__main__":
    file_paths = get_all_csv_filepaths()
    final_df = pd.DataFrame()

    with Progress() as progress:
        for file_path in file_paths:
            result_df = process_file(file_path, chunk_size=10000, progress=progress)
            final_df = pd.concat([final_df, result_df], ignore_index=True)

    print(final_df["判决时间"].dt.year.value_counts().sort_index())
    print(final_df["判决时间"].dt.month.value_counts().sort_index())
