#!/usr/bin/env python3
"""
批量更新代码中的硬编码 API key 为环境变量
"""
import os
import re
from pathlib import Path

def update_api_keys_in_file(file_path: Path):
    """更新单个文件中的 API key"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已经导入 os
        has_os_import = 'import os' in content

        # 查找 DeepSeek API key 模式
        deepseek_pattern = r'api_key="sk-a19832c6da69445d9f05d04116e0636c"'
        if re.search(deepseek_pattern, content):
            # 添加 os 导入（如果还没有）
            if not has_os_import:
                # 找到第一个 import 语句，在它之前添加 os 导入
                import_match = re.search(r'^import|^from.*import', content, re.MULTILINE)
                if import_match:
                    insert_pos = import_match.start()
                    content = content[:insert_pos] + 'import os\n' + content[insert_pos:]
                else:
                    # 如果没有找到 import，在文件开头添加
                    content = 'import os\n' + content

            # 替换 API key
            content = re.sub(deepseek_pattern, 'api_key=os.getenv("DEEPSEEK_API_KEY")', content)

            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[OK] 更新了 {file_path}")
            return True
        else:
            return False

    except Exception as e:
        print(f"[ERROR] 处理 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    if not src_dir.exists():
        print(f"[ERROR] 找不到源代码目录: {src_dir}")
        return

    updated_files = []

    # 遍历所有 Python 文件
    for py_file in src_dir.rglob("*.py"):
        if update_api_keys_in_file(py_file):
            updated_files.append(py_file)

    if updated_files:
        print(f"\n[SUCCESS] 成功更新了 {len(updated_files)} 个文件:")
        for file_path in updated_files:
            print(f"  - {file_path.relative_to(project_root)}")
        print("\n[INFO] 请记得设置环境变量 DEEPSEEK_API_KEY")
    else:
        print("[INFO] 没有找到需要更新的文件")

if __name__ == "__main__":
    main()
