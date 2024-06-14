def remove_duplicates(filename):
    lines_seen = set()
    output_filename = filename.split('.')[0] + "_nodupes.txt"

    with open(filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        for line in input_file:
            line = line.strip()  # 去除行尾的换行符和空格
            if line not in lines_seen:
                output_file.write(line + '\n')
                lines_seen.add(line)

    print("去除重复行完成！保存为：", output_filename)
