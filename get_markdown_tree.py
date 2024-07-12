"""
2024-09-15
讲目录下的 *.md 文件生成目录树

方便 vuepress 来用
运行: pnpm vuepress dev


2024-05-09 09:29:39
这个 _2 是主要给我的linux 使用的

"""

import re
import os
import sys
import requests
import json
import time

from pathlib import Path
from addict import Dict


def load_json(jsfile="y.json"):
    if not Path(jsfile).exists() or os.path.getsize(jsfile) == 0:
        with open(jsfile, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
        print(
            f"文件{jsfile}不存在或者为空，已经创建_ 如果是项目初始化阶段，这不该出现此提示"
        )
    with open(jsfile, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return Dict(data)
    return data


def save_json(data, jsfile="y.json"):
    Path(jsfile).parent.mkdir(parents=True, exist_ok=True)
    with open(jsfile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_md(md_data, filename="readme.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_data)


class GetPath2:
    """
    这个的话我希望的是直接用 # 号进行分类, 每个里面又搞一个 readme.md 单独 作为一个子页面

    """

    def __init__(
        self,
        target_dirs=[],
        no_dir=["venv", ".git", "build", "dist"],
        init_str="",
        tofile="readme.md",
        iscommit=1,
    ):
        """
        args:
            target_dirs: 目标目录(我这里直接要的是目录列表, 故而可以多个目录)
            no_dir: 需要跳过的目录
            init_str: 在markdown 前面添加的字符串
            iscommit: 是否给 md 添加评论功能

        """
        self.no_dir = no_dir
        if not target_dirs:
            # 指定目标目录列表
            target_dirs = [
                "./note2/",
            ]
        if len(target_dirs) == 1 and target_dirs[0] == "*":
            target_dirs = [f"{i}" for i in os.listdir("./") if os.path.isdir(f"./{i}")]
            target_dirs = [i for i in target_dirs if i not in self.no_dir]
            target_dirs.insert(0, "./")
        self.target_dirs = target_dirs
        # 生成目录树
        directory_tree = ""
        if init_str:
            directory_tree += init_str
            directory_tree += "\n"
            directory_tree += "\n"
        directory_tree += f"## 大纲\n\n"
        directory_tree += f"{self.generate_directory_toc(target_dirs)}\n\n"
        for dir_i, dir in enumerate(target_dirs):
            if self.has_markdown_files(dir):
                # directory_tree += f"{self.generate_directory_toc(dir)}\n\n"
                directory_tree += f"---\n\n"
                directory_tree += self.generate_directory_tree(dir)
                directory_tree += "\n"
        directory_tree += "<CommentService/>"  # 这个是给后面的评论系统用的
        directory_tree += "\n"

        # 输出为Markdown格式
        markdown_output = f"# 目录树\n\n{directory_tree}"
        write_md(markdown_output, tofile)
        if iscommit:
            self.all_add_commit()

    def generate_directory_toc(self, root_dirs: list, header_n=0):
        """
        这个是 toc 的主逻辑

        这个就只要目录
        """
        if isinstance(root_dirs, str):
            root_dirs = [root_dirs]
        r1_str = ""
        if root_dirs[0] == "./":
            root_dirs = [root_dirs[0]]
        for root_dir in root_dirs:
            if root_dir[0] == "/":
                print("怎么会有/ 的目录，快去维护一下代码_err:001")
                continue
            files = []
            dirs = []
            # 1. [docker\_k8s](#docker_k8s)
            index_dir_name = Path(root_dir).name
            if not index_dir_name:
                index_dir_name = "根目录"
            r_str = "    " * header_n + "- " + index_dir_name
            r_str = f'{"    "*header_n}{"- "}[{index_dir_name}](#{index_dir_name})\n'

            # # 遍历目录下的文件和子目录 (也同时为后面做准备)
            l_dir = [i for i in os.listdir(root_dir)]
            for item in sorted(
                l_dir,
                key=lambda item: (
                    int(re.search(r"(\d+)", item).group(1))
                    if re.search(r"(\d+)", item)
                    else 0
                ),
            ):
                item_path = os.path.join(root_dir, item)
                if os.path.isfile(item_path):
                    if item.endswith(".md"):
                        files.append(item)
                elif os.path.isdir(item_path):
                    if self.has_markdown_files(item_path):
                        dirs.append(item)

            # 递归处理子目录
            for i, directory in enumerate(dirs):
                if Path(directory).name in self.no_dir:
                    continue
                r_str += self.generate_directory_toc(
                    [os.path.join(root_dir, directory)], header_n=header_n + 1
                )
            r1_str += r_str
        return r1_str

    def generate_directory_tree(self, root_dir, header="##"):
        """
        这里才该是主逻辑

        如果当前有 md 就先搞了， 如果是有子集，就最后把子集一起搞了，然后添加到这里来

        """
        files = []
        dirs = []
        index_dir_name = Path(root_dir).name
        if not index_dir_name:
            index_dir_name = "根目录"
        r_str = header + " " + index_dir_name + "\n\n"

        # # 遍历目录下的文件和子目录 (也同时为后面做准备)
        l_dir = [i for i in os.listdir(root_dir)]
        for item in sorted(
            l_dir,
            key=lambda item: (
                int(re.search(r"(\d+)", item).group(1))
                if re.search(r"(\d+)", item)
                else 0
            ),
        ):
            item_path = os.path.join(root_dir, item)
            if os.path.isfile(item_path):
                if item.endswith(".md"):
                    files.append(item)
            elif os.path.isdir(item_path):
                if self.has_markdown_files(item_path):
                    dirs.append(item)

        # 输出当前目录下的文件
        for i, file in enumerate(files):
            file_path = os.path.join(root_dir, file)
            relative_path = os.path.relpath(file_path, start="./")
            relative_path = file_path.replace("\\", "/")
            r_str += f"- [{file}]({relative_path})\n"
            if i == len(files) - 1:
                r_str += "\n"

        # 递归处理子目录
        for i, directory in enumerate(dirs):
            if Path(directory).name in self.no_dir:
                continue
            r_str += self.generate_directory_tree(
                os.path.join(root_dir, directory), header=header + "#"
            )
        return r_str

    def has_markdown_files(self, directory):
        for parent, dirnames, filenames in os.walk(directory):
            if any(filename.endswith(".md") for filename in filenames):
                return True
        return False

    def all_add_commit(self):
        """
        给所有的 md 添加评论 <CommentService/>
        """
        old_commit_data = load_json("commit_data.json")
        # 获取目录下所有 .md 的文件
        all_md = []
        for root_path in self.target_dirs:
            for root, dirs, files in os.walk(root_path):
                for file in files:
                    if file.endswith(".md"):
                        path1 = Path(root) / file
                        file_size = os.path.getsize(path1)
                        if file_size > 10:
                            if str(path1) in old_commit_data:
                                if old_commit_data[str(path1)] == file_size:
                                    continue
                            all_md.append([path1, file_size])

        for md in all_md:
            try:
                with open(md[0], "r", encoding="utf-8") as f:
                    data = f.read()
                if "<CommentService/>" in data:
                    continue
                data += "\n<CommentService/>\n"
                with open(md[0], "w", encoding="utf-8") as f:
                    f.write(data)
                old_commit_data[str(md[0])] = os.path.getsize(md[0])
            except Exception as e:
                print(f"{md[0]}--没有被添加评论(因为错误)")
        save_json(old_commit_data, "commit_data.json")


def create_config_path(port="30003", title="Note1", description="Book_note", *args):
    """
    创建配置文件
    .vuepress
        config.ts
    """
    file_ = requests.get(
        "https://pscly.cn/files/config.ts_py",
        proxies={"http": None, "https": None},
    )
    data = file_.text
    data = data.replace("{{1}}", port)
    data = data.replace("{{2}}", title)
    data = data.replace("{{3}}", description)
    if not Path(".vuepress/config.ts").exists():
        Path(".vuepress").mkdir(parents=True, exist_ok=True)
        with open(".vuepress/config.ts", "w", encoding="utf-8") as f:
            for len_data in data.split("\n"):
                f.writelines(len_data)
    return


if __name__ == "__main__":
    is_while = 1
    while is_while:
        # GetPath2(['./testnote/'])
        print("开始 运行" + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        GetPath2(
            ["*"],
            [
                "venv",
                ".git",
                "build",
                "dist",
                "md-images",
                "md_datas",
                "Book_code1",
                "node_modules",
                "qt",
                "qt2",
                ".obsidian",
                "venv",
                ".vscode",
                "RECYCLE.BIN",
            ],
            "> 数据可以在 [这里](https://u.pscly.icu:33090/pscly/note1) 找到\n\n**建议使用左侧的目录树**",
            iscommit=0,
            tofile="readme.md",
        )

        args1 = sys.argv[1:]
        if args1:
            print("似乎是有参数的运行，所以就不搞循环了")
            if len(args1) == 1:
                is_while = 0
                break
                # 代表这个是有 1init 来控制的循环
            create_config_path(*args1)
            break
        print("运行结束，等待下次循环")
        print("等待60s")
        # 进度条
        print("-" * 25)
        for i in range(25):
            print(f"#".expandtabs(100) * (i + 1), end="\r")
            time.sleep(2.5)
        print("")

# TODO:# 2024-07-03 16:47:09 如果是去了 .. 目录，那么目录链接就不行了
