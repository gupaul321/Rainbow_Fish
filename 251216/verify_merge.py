import pandas as pd
import os

def verify_logic():
    # ID 리스트 파일 경로
    id_file_path = 'sampled_ids_full_list.txt'
    
    if not os.path.exists(id_file_path):
        print(f"Error: {id_file_path} not found.")
        return

    # 파일 읽기
    with open(id_file_path, 'r') as f:
        sampled_ids = [line.strip() for line in f.readlines()]
    print(f"Loaded {len(sampled_ids)} IDs.")

    # 데이터 파일이 있는 디렉토리 경로
    data_dir = '../../data/03.카드 승인매출정보'
    if not os.path.exists(data_dir):
        print(f"Error: {data_dir} not found.")
        return

    # 월별 데이터 파일 리스트 (201807 ~ 201812)
    months = ['201807', '201808', '201809', '201810', '201811', '201812']
    file_pattern = '{month}_승인매출정보.csv'

    dfs = []

    for month in months:
        file_name = file_pattern.format(month=month)
        file_path = os.path.join(data_dir, file_name)
        
        if os.path.exists(file_path):
            print(f"Loading {month}...")
            # For verification, just read a few rows or columns to speed up, but user logic reads all.
            # reading full file might be slow for testing, but necessary for correct count.
            # I will read nrows=1000 to verify the code runs, not the full merge which might crash memory or take too long here.
            df_temp = pd.read_csv(file_path, nrows=10000) 
            
            # ID 필터링
            df_filtered = df_temp[df_temp['발급회원번호'].isin(sampled_ids)]
            print(f"  {month}: {df_temp.shape} -> {df_filtered.shape}")
            
            dfs.append(df_filtered)
        else:
            print(f"Warning: {file_path} not found")

    if dfs:
        df_merged = pd.concat(dfs, axis=0, ignore_index=True)
        print("Merge successful.")
        print(f"Merged shape from sample: {df_merged.shape}")
    else:
        print("No data merged.")

if __name__ == "__main__":
    verify_logic()
