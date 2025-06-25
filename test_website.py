#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站测试脚本 - 验证二维码链接是否正常
"""

import requests
import time

def test_url(url, name):
    """测试URL是否可访问"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name}: {url} (状态码: {response.status_code})")
            return True
        else:
            print(f"⚠️ {name}: {url} (状态码: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name}: {url} (错误: {e})")
        return False

def main():
    """测试所有二维码链接"""
    base_url = "http://127.0.0.1:5000"
    
    test_urls = [
        ("网站首页", f"{base_url}/"),
        ("PPT专用版", f"{base_url}/ppt"),
        ("商业计划书", f"{base_url}/business"),
        ("苹果演示", f"{base_url}/apple_style_demo.html"),
    ]
    
    print("🌐 开始测试娃改坊网站链接...")
    print("=" * 50)
    
    success_count = 0
    
    for name, url in test_urls:
        if test_url(url, name):
            success_count += 1
        time.sleep(0.5)  # 避免请求过于频繁
    
    print("=" * 50)
    print(f"🎯 测试结果: {success_count}/{len(test_urls)} 个链接正常")
    
    if success_count == len(test_urls):
        print("🎉 所有链接正常，二维码可以放心使用！")
        print("💡 建议:")
        print("   - 网站首页: 完整功能展示，适合主要演示")
        print("   - PPT专用版: 简化版本，加载更快")
        print("   - 苹果演示: 技术实力展示，视觉效果佳")
    else:
        print("⚠️ 部分链接无法访问，请检查:")
        print("   - 确保运行了 python app.py")
        print("   - 检查端口5000是否被占用")
        print("   - 确认防火墙设置")
    
    print("\n📱 手机测试建议:")
    print("   - 用微信扫一扫测试二维码")
    print("   - 确认手机和电脑在同一WiFi网络")
    print("   - 建议横屏浏览获得最佳体验")

if __name__ == "__main__":
    main() 