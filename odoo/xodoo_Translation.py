import os
import re
from pathlib import Path


def process_translation_file(file_path):
    """处理单个翻译文件"""
    with open(file_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()

        # 检查首行有效性
        if not lines or not lines[0].startswith("# Translation of Odoo Server."):
            return False

        # 定位Plural-Forms行
        plural_idx = None
        for idx, line in enumerate(lines):
            if line.strip().startswith("Plural-Forms:"):
                plural_idx = idx
                break

        if plural_idx is None:
            return False  # 没有Plural-Forms行则跳过

        # 跳过后续空行
        start_idx = plural_idx + 1
        while start_idx < len(lines) and lines[start_idx].strip() == '':
            start_idx += 1

        # 构建新内容：首行 + 有效内容
        new_content = [lines[0]] + lines[start_idx:]

        # 原子化写入
        f.seek(0)
        f.truncate()
        f.writelines(new_content)
        return True


def batch_process_translations(root_path):
    """批量处理翻译文件"""
    processed_count = 0
    for root, _, files in os.walk(root_path):
        if not root.endswith('i18n'):
            continue

        for file in files:
            if not file.lower().endswith(('.po', '.pot')):
                continue

            file_path = Path(root) / file
            try:
                if process_translation_file(file_path):
                    print(f"处理成功：{file_path}")
                    processed_count += 1
            except Exception as e:
                print(f"处理失败 {file_path}：{str(e)}")

    print(f"处理完成！共清理 {processed_count} 个文件")


if __name__ == "__main__":
    MODULES_PATH = "/Users/amos/Documents/github/xodoo/xodoo/odoo/addons"
    batch_process_translations(MODULES_PATH)

    #
    # 从路径/Users/amos/Documents/github/xodoo/xodoo/odoo/addons 模块下,每一个模块下的i18n 找所有后缀是 *.po 与 *.pot
    # 读取文件第一行是 # Translation of Odoo Server. 一直向下读取只到读取匹配到 "Plural-Forms: 执行删除他们之间的信息，但保留第一行 匹配的Plural-Forms 也要删除
    # 如果一个文件中配置不到 Plural-Forms: 那么就忽略这个文件
    # 按上面的条件用python帮我写一个批处理工具
    #

