from os import listdir
from os.path import isfile, join

def find_missing_files(directory, total_pages, split):
    all_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    missing_files = []

    for page in range(1, total_pages + 1):
        expected_files = [f"{page}.webp"] + [f"{page} ({i}).webp" for i in range(1, split)]
        for file in expected_files:
            if file not in all_files:
                missing_files.append(file)

    return missing_files

# 设置参数
directory = 'temp/'
total_pages = 300
split = 6

# 调用函数并输出结果
missing_files = find_missing_files(directory, total_pages, split)
print(f"缺少文件数量{len(missing_files)},缺少的文件编号如下：")
for file in missing_files:
    print(file)
