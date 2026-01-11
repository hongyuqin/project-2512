#!/usr/bin/env python3
"""
项目设置脚本
用于初始化项目环境和依赖
"""
import subprocess
import sys
from pathlib import Path

def run_command(command: str, description: str):
    """运行命令并显示状态"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def main():
    """主设置流程"""
    project_root = Path(__file__).parent.parent

    print("🚀 开始设置 project-2512 项目环境")
    print(f"📁 项目根目录: {project_root}")

    # 检查 Python 版本
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ 需要 Python 3.8+，当前版本: {python_version.major}.{python_version.minor}")
        return False

    print(f"✅ Python 版本检查通过: {python_version.major}.{python_version.minor}.{python_version.micro}")

    # 创建必要的目录
    dirs_to_create = ["tmp", "logs"]
    for dir_name in dirs_to_create:
        dir_path = project_root / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"📁 创建目录: {dir_name}")

    # 安装依赖
    if not run_command("pip install -r requirements.txt", "安装项目依赖"):
        return False

    # 安装开发依赖（可选）
    dev_install = input("是否安装开发依赖？(y/N): ").lower().strip()
    if dev_install == 'y':
        if not run_command("pip install -e '.[dev]'", "安装开发依赖"):
            return False

    # 检查数据库文件
    db_files = ["tmp/agents.db", "tmp/data.db"]
    for db_file in db_files:
        db_path = project_root / db_file
        if not db_path.exists():
            print(f"ℹ️  数据库文件不存在，将在使用时自动创建: {db_file}")

    print("\n🎉 项目环境设置完成！")
    print("\n📝 下一步:")
    print("1. 配置环境变量 (.env 文件)")
    print("2. 运行示例: cd examples && python minimax_tts_example.py")
    print("3. 查看 README.md 了解更多用法")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
