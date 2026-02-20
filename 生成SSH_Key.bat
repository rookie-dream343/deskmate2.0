@echo off
echo ============================================
echo SSH Key 生成工具
echo ============================================
echo.

REM 检查 ssh-keygen 是否可用
where ssh-keygen >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 ssh-keygen 命令
    echo 请确保已安装 Git for Windows
    echo.
    pause
    exit /b 1
)

echo 正在生成 SSH Key...
echo.

REM 生成 SSH key (ED25519 格式，更安全)
ssh-keygen -t ed25519 -C "deskmate@computer" -f %USERPROFILE%\.ssh\id_ed25519 -N ""

if errorlevel 1 (
    echo.
    echo 生成失败！
    pause
    exit /b 1
)

echo.
echo ============================================
echo SSH Key 生成成功！
echo ============================================
echo.
echo 你的 SSH 公钥 (复制下面整行):
echo ============================================
type %USERPROFILE%\.ssh\id_ed25519.pub
echo ============================================
echo.

REM 启动 GitHub 添加页面
start https://github.com/settings/keys

echo.
echo 接下来请:
echo 1. 在打开的网页上点击 [New SSH key]
echo 2. Title 填写: My Computer
echo 3. Key 粘贴上面显示的 SSH 公钥 (整行)
echo 4. 点击 [Add SSH key]
echo 5. 完成后运行: ssh -T git@github.com
echo.
echo 按任意键退出...
pause >nul
