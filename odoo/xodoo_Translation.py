import os
import xlwt


def read_manifest(file_path):
    """读取并解析 __manifest__.py 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        manifest_content = f.read()
    return eval(manifest_content)


def extract_manifest_info(manifest_dict):
    """提取 manifest 信息（包含所有字段）"""
    return {
        'name': manifest_dict.get('name', ''),
        'version': manifest_dict.get('version', ''),
        'category': manifest_dict.get('category', ''),
        'summary': manifest_dict.get('summary', ''),
        'sequence': manifest_dict.get('sequence', 0),
        'author': manifest_dict.get('author', ''),
        'website': manifest_dict.get('website', ''),
        'license': manifest_dict.get('license', ''),
        'depends': ', '.join(manifest_dict.get('depends', [])),  # 转换为字符串
        'description': manifest_dict.get('description', 'N/A').replace('\n', ' ')  # 处理换行符
    }


def export_to_xls(data, output_path):
    """将数据导出到 Excel 文件"""
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Modules')

    # 定义表头
    headers = [
        '模块名称', '版本', '分类', '摘要',
        '顺序', '作者', '网站', '许可证',
        '依赖模块', '详细描述'
    ]

    # 写入表头
    for col, header in enumerate(headers):
        sheet.write(0, col, header)

    # 写入数据
    for row, item in enumerate(data, 1):
        sheet.write(row, 0, item['name'])
        sheet.write(row, 1, item['version'])
        sheet.write(row, 2, item['category'])
        sheet.write(row, 3, item['summary'])
        sheet.write(row, 4, item['sequence'])
        sheet.write(row, 5, item['author'])
        sheet.write(row, 6, item['website'])
        sheet.write(row, 7, item['license'])
        sheet.write(row, 8, item['depends'])
        sheet.write(row, 9, item['description'])

    workbook.save(output_path)


def process_manifests(folder_path, output_file):
    """主处理函数"""
    all_modules = []

    for root, dirs, files in os.walk(folder_path):
        if '__manifest__.py' in files:
            manifest_path = os.path.join(root, '__manifest__.py')
            manifest_data = read_manifest(manifest_path)
            module_info = extract_manifest_info(manifest_data)
            all_modules.append(module_info)

    export_to_xls(all_modules, output_file)
    print(f"成功导出 {len(all_modules)} 个模块信息到 {output_file}")


if __name__ == "__main__":
    # 配置路径
    ODOO_MODULES_PATH = "/Users/amos/Documents/Gitee/xodoo/xodoo_xodoo"  # 你的模块目录
    OUTPUT_XLS = "odoo_modules.xls"  # 输出文件名

    process_manifests(ODOO_MODULES_PATH, OUTPUT_XLS)