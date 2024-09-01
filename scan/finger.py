import subprocess,ast,os,shutil

def find_latest(dir_path):
    latest_time = 0
    latest_file = None

    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)

        if os.path.isfile(full_path):
            creation_time = os.path.getctime(full_path)

            if creation_time > latest_time:
                latest_time = creation_time
                latest_file = filename

    return latest_file

def domains_cms(file_name):

    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)

    finger_path = config['finger_path']
    thread = input("线程数：")

    with open(f"{finger_path}/config/config.py","r",encoding="utf-8") as finger_config_file:
        config_lines = finger_config_file.readlines()

    for num,line in enumerate(config_lines):
        if "threads" in line:
            config_lines[num] = f"threads = {thread}"

    with open(f"{finger_path}/config/config.py","w",encoding="utf-8") as finger_config_outfile:
        finger_config_outfile.writelines(config_lines)

    command = ['python', f'{finger_path}/Finger.py', '-f', file_name]
    print(f"正在收集指纹信息，请耐心等待！")
    try:
        subprocess.run(command, capture_output=True, text=True,encoding='utf-8')
    except Exception as e:
        print(f"输出：{e}")
    lateast_file_name = find_latest(f"{finger_path}/output")
    shutil.move(f"{finger_path}/output/{lateast_file_name}",f"./{file_name.replace('.txt','.xlsx')}")
    print("收集完毕")
