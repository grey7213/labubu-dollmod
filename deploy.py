#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
娃改坊项目自动化部署脚本
自动创建GitHub仓库并部署到Render.com
"""

import os
import subprocess
import webbrowser
from pathlib import Path

def print_step(step_num, title, description=""):
    """打印步骤信息"""
    print(f"\n🚀 步骤 {step_num}: {title}")
    if description:
        print(f"   {description}")
    print("-" * 50)

def check_git():
    """检查Git是否安装"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git未安装，请先安装Git: https://git-scm.com/")
        return False

def check_files():
    """检查必要文件是否存在"""
    required_files = [
        "app.py",
        "requirements.txt", 
        "Procfile",
        "runtime.txt",
        "templates/index.html",
        "templates/business.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必要文件检查完成")
    return True

def init_git_repo():
    """初始化Git仓库"""
    try:
        # 检查是否已经是Git仓库
        subprocess.run(["git", "status"], capture_output=True, check=True)
        print("✅ Git仓库已存在")
        return True
    except subprocess.CalledProcessError:
        # 初始化新仓库
        try:
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "🚀 初始化娃改坊商业计划书项目"], check=True)
            print("✅ Git仓库初始化完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Git初始化失败: {e}")
            return False

def create_readme():
    """创建README.md文件"""
    readme_content = """# 🎯 娃改坊商业计划书

## 项目简介
娃改坊专注于LABUBU等热门潮玩IP的轻量化改装配件，销售"社交身份增强服务"。

## 在线演示
- 📊 数据洞察首页: [点击访问](/)
- 📋 商业计划书: [点击访问](/business)
- 📱 PPT专用版: [点击访问](/ppt)
- 🍎 苹果风格展示: [点击访问](/apple_style_demo.html)

## 核心数据
- LABUBU销售增长率: 1289%
- 2024年销售额: 45.8亿元
- 改装配件利润率: 500%+
- 启动资金需求: ≤1万元

## 技术栈
- 后端: Flask + PyEcharts
- 前端: HTML5 + CSS3 + JavaScript
- 数据可视化: ECharts
- 部署: Render.com

## 本地运行
```bash
pip install -r requirements.txt
python app.py
```

## 联系我们
- 📧 商务合作: dollmodshop@163.com
- 📱 创始人微信: DollMod2025

© 2025 娃改坊 DollModShop | 让每个LABUBU都独一无二 ✨
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ README.md创建完成")

def main():
    """主函数"""
    print("🎯 娃改坊项目自动化部署助手")
    print("=" * 50)
    
    # 步骤1: 检查环境
    print_step(1, "环境检查", "检查Git安装和必要文件")
    if not check_git() or not check_files():
        return
    
    # 步骤2: 创建README和Git仓库
    print_step(2, "Git仓库准备", "创建README文件和初始化Git仓库")
    create_readme()
    if not init_git_repo():
        return
    
    # 步骤3: 部署指导
    print_step(3, "云部署指导", "接下来需要手动完成GitHub和Render部署")
    
    print("""
📋 接下来的步骤:

1️⃣ 创建GitHub仓库:
   - 访问 https://github.com/new
   - 仓库名称: labubu-dollmod
   - 选择Public
   - 不要勾选README（我们已经创建了）
   - 点击"Create repository"

2️⃣ 推送代码到GitHub:
   复制并执行以下命令:
   
   git remote add origin https://github.com/YOUR_USERNAME/labubu-dollmod.git
   git branch -M main
   git push -u origin main
   
   ⚠️ 记得将YOUR_USERNAME替换为你的GitHub用户名

3️⃣ 部署到Render:
   - 访问 https://render.com
   - 注册账号（可用GitHub登录）
   - 点击 "New" → "Web Service"
   - 连接刚创建的GitHub仓库
   - 部署配置会自动检测，直接点击"Create Web Service"

4️⃣ 获取部署地址:
   部署成功后，你会得到类似这样的地址:
   https://labubu-dollmod.onrender.com
   
   将这个地址更新到你的PPT中！

💡 小贴士:
   - 免费版本首次访问可能需要30秒启动时间
   - Render会自动为你配置HTTPS
   - 每次GitHub更新代码，Render会自动重新部署
    """)
    
    # 询问是否自动打开相关网站
    response = input("\n🤔 是否自动打开GitHub和Render网站? (y/n): ").lower()
    if response in ['y', 'yes', 'Y']:
        print("🌐 正在打开相关网站...")
        webbrowser.open("https://github.com/new")
        webbrowser.open("https://render.com")
    
    print("\n🎉 准备工作完成！请按照上述步骤完成云部署。")
    print("📚 详细指南请查看: 云部署指南.md")

if __name__ == "__main__":
    main() 