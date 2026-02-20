#!/usr/bin/env python3
"""
快速生成 SSH Key 并显示添加到 GitHub 的步骤
"""

import subprocess
import os
import sys

def generate_ssh_key():
    """生成 SSH key"""
    print("=" * 50)
    print("SSH Key 生成工具")
    print("=" * 50)

    # 检查是否已存在
    ssh_dir = os.path.expanduser("~/.ssh")
    key_file = os.path.join(ssh_dir, "id_ed25519")

    if os.path.exists(key_file):
        print(f"\n✓ SSH key 已存在: {key_file}")
        choice = input("是否要重新生成？(y/N): ").lower()
        if choice != 'y':
            show_existing_key()
            return

    print("\n正在生成 SSH key...")

    # 生成 SSH key
    keygen_cmd = [
        "ssh-keygen",
        "-t", "ed25519",
        "-C", "deskmate@computer",
        "-f", key_file,
        "-N", ""
    ]

    try:
        subprocess.run(keygen_cmd, check=True)
        print(f"\n✓ SSH key 生成成功!")
        print(f"  私钥: {key_file}")
        print(f"  公钥: {key_file}.pub")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 生成失败: {e}")
        print("\n请确保已安装 Git（包含 ssh-keygen）")
        return

    # 显示公钥
    show_existing_key()

    # 显示添加步骤
    show_github_instructions()

def show_existing_key():
    """显示现有的 SSH 公钥"""
    ssh_dir = os.path.expanduser("~/.ssh")
    pub_key_file = os.path.join(ssh_dir, "id_ed25519.pub")

    if not os.path.exists(pub_key_file):
        pub_key_file = os.path.join(ssh_dir, "id_rsa.pub")

    if os.path.exists(pub_key_file):
        print("\n" + "=" * 50)
        print("你的 SSH 公钥 (复制下面整行):")
        print("=" * 50)
        with open(pub_key_file, 'r') as f:
            key_content = f.read().strip()
            print(key_content)
        print("=" * 50)

        # 保存到剪贴板（Windows）
        try:
            import pyperclip
            pyperclip.copy(key_content)
            print("\n✓ 已自动复制到剪贴板!")
        except ImportError:
            print("\n提示: 安装 pyperclip 可自动复制 (pip install pyperclip)")
    else:
        print("\n✗ 未找到 SSH 公钥文件")

def show_github_instructions():
    """显示 GitHub 添加步骤"""
    print("\n" + "=" * 50)
    print("添加 SSH Key 到 GitHub 的步骤:")
    print("=" * 50)
    print("1. 打开浏览器，访问:")
    print("   https://github.com/settings/keys")
    print("\n2. 点击 [New SSH key] 或 [Add SSH key]")
    print("\n3. Title 填写: My Computer")
    print("\n4. Key 粘贴上面显示的 SSH 公钥")
    print("\n5. 点击 [Add SSH key]")
    print("\n完成后，运行以下命令测试连接:")
    print("   ssh -T git@github.com")
    print("=" * 50)

if __name__ == "__main__":
    generate_ssh_key()
    input("\n按回车退出...")
