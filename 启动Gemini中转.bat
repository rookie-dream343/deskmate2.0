@echo off
echo ============================================
echo Gemini API 中转服务
echo ============================================
echo.

REM 激活 conda 环境
call D:\conda\Scripts\activate.bat D:\conda\envs\my-neuro

REM 安装依赖（如果还没有）
echo 检查依赖...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 正在安装 Flask...
    pip install flask requests -i https://pypi.tuna.tsinghua.edu.cn/simple/
)

echo.
echo 启动中转服务...
echo.

REM 启动中转服务
python gemini_proxy.py

pause
