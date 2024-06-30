from typing import Generator

import pandas as pd
from rich.progress import Progress

from utils import get_all_csv_filepaths


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
        filtered_chunk = chunk[chunk["文书内容"].notnull()].copy()
        filtered_chunk.loc[:, "出生年月"] = filtered_chunk["文书内容"].str.extract(
            r"(\d{4}年\d{1,2}月\d{1,2}日)"
        )
        # 将日期格式转换为datetime格式
        filtered_chunk["出生年月"] = pd.to_datetime(
            filtered_chunk["出生年月"], format="%Y年%m月%d日", errors="coerce"
        )
        # 删除”出生年月“列中的空行
        filtered_chunk = filtered_chunk[filtered_chunk["出生年月"].notnull()]
        # 保留”出生年月“列中相对当前时间的18-25岁的数据
        filtered_chunk = filtered_chunk[
            (pd.Timestamp.now() - filtered_chunk["出生年月"]).dt.days / 365.25 >= 18
        ]
        filtered_chunk = filtered_chunk[
            (pd.Timestamp.now() - filtered_chunk["出生年月"]).dt.days / 365.25 <= 25
        ]

        progress.advance(task)

    return filtered_df


if __name__ == "__main__":
    file_paths = get_all_csv_filepaths()
    final_df = pd.DataFrame()

    with Progress() as progress:
        for file_path in file_paths:
            result_df = process_file(file_path, chunk_size=10000, progress=progress)
            final_df = pd.concat([final_df, result_df], ignore_index=True)
