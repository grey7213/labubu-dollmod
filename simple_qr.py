#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版二维码生成器 - 娃改坊PPT专用
"""

import qrcode
import os

def generate_simple_qr(url, filename):
    """生成简单的二维码"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#2D3748", back_color="#FFFFFF")
    img.save(filename)
    print(f"✅ 生成: {filename}")

def main():
    """生成PPT需要的二维码"""
    
    # 创建输出目录
    if not os.path.exists("qr_codes"):
        os.makedirs("qr_codes")
        print("📁 创建目录: qr_codes")
    
    base_url = "https://labubu-dollmod.onrender.com"
    
    # 生成二维码
    qr_list = [
        ("网站首页", f"{base_url}/", "娃改坊_网站首页.png"),
        ("PPT专用版", f"{base_url}/ppt", "娃改坊_PPT版本.png"), 
        ("商业计划书", f"{base_url}/business", "娃改坊_商业计划.png"),
        ("苹果演示", f"{base_url}/apple_style_demo.html", "娃改坊_技术演示.png"),
    ]
    
    print("🎯 开始生成娃改坊二维码...")
    print("=" * 40)
    
    for name, url, filename in qr_list:
        filepath = os.path.join("qr_codes", filename)
        try:
            generate_simple_qr(url, filepath)
            print(f"📱 {name}: {url}")
        except Exception as e:
            print(f"❌ {name} 生成失败: {e}")
    
    print("=" * 40)
    print("🎉 二维码生成完成！")
    print("📁 文件位置: qr_codes/")
    print("\n📋 PPT使用建议:")
    print("⭐ 推荐使用: 娃改坊_网站首页.png")
    print("⭐ 技术展示: 娃改坊_技术演示.png") 
    print("⭐ PPT版本: 娃改坊_PPT版本.png")
    
    # 生成说明文件
    with open("qr_codes/使用说明.txt", "w", encoding="utf-8") as f:
        f.write("""
🎯 娃改坊PPT二维码使用指南

生成的文件：
- 娃改坊_网站首页.png (推荐)
- 娃改坊_PPT版本.png (推荐)  
- 娃改坊_商业计划.png
- 娃改坊_技术演示.png (推荐)

PPT嵌入步骤：
1. 在PPT中选择 插入 → 图片 → 从文件
2. 选择对应的PNG文件
3. 调整大小为 2-3cm
4. 放置在适当位置

演示话术：
"请扫描二维码现场体验我们的数据洞察平台，感受娃改坊的技术实力"

注意事项：
- 确保网站服务运行中 (python app.py)
- 测试二维码扫描是否正常
- 准备网络断开时的备用方案
        """)
    
    print("📄 使用说明已保存到: qr_codes/使用说明.txt")

if __name__ == "__main__":
    main() 