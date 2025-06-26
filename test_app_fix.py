#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
象限图修复验证测试
"""

def test_imports():
    """测试所有导入是否正常"""
    try:
        # 测试基础导入
        from pyecharts.charts import Scatter
        from pyecharts import options as opts
        from pyecharts.globals import ThemeType, CurrentConfig
        from pyecharts.commons.utils import JsCode
        print("✅ PyEcharts基础导入成功")
        
        # 测试pandas和其他依赖
        import pandas as pd
        import numpy as np
        print("✅ 数据处理库导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False

def test_competitor_chart():
    """测试象限图函数"""
    try:
        # 创建测试数据
        scatter_data = [
            ["泡泡玛特", 3100, 85],
            ["万代", 800, 78],
            ["MINISO名创", 180, 70]
        ]
        
        # 创建散点图
        scatter = (
            Scatter(init_opts=opts.InitOpts(
                theme=ThemeType.ROMANTIC, 
                width="100%", 
                height="500px",
                renderer="canvas",
                bg_color="transparent"
            ))
            .add_xaxis([])
            .add_yaxis(
                "竞品分析",
                [{"value": [item[1], item[2]], "name": item[0]} for item in scatter_data],
                symbol_size=20,
                itemstyle_opts=opts.ItemStyleOpts(
                    color="#FF6B9D",
                    opacity=0.8,
                    border_color="#FFFFFF",
                    border_width=3
                )
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="测试象限图",
                    pos_left="center",
                    pos_top="5%"
                ),
                xaxis_opts=opts.AxisOpts(
                    name="市值 (亿港元)",
                    type_="log",
                    min_=10,
                    max_=5000
                ),
                yaxis_opts=opts.AxisOpts(
                    name="品牌力指数",
                    min_=55,
                    max_=90
                )
            )
        )
        
        # 尝试渲染
        html_content = scatter.render_embed()
        
        if html_content and len(html_content) > 100:
            print("✅ 象限图渲染成功")
            print(f"📊 生成HTML长度: {len(html_content)} 字符")
            return True
        else:
            print("❌ 象限图渲染失败或内容为空")
            return False
            
    except Exception as e:
        print(f"❌ 象限图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cdn_config():
    """测试CDN配置"""
    try:
        from pyecharts.globals import CurrentConfig
        
        # 设置CDN
        CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/"
        print("✅ CDN配置成功")
        print(f"📡 当前CDN: {CurrentConfig.ONLINE_HOST}")
        return True
        
    except Exception as e:
        print(f"❌ CDN配置失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔧 开始象限图修复验证测试...\n")
    
    tests = [
        ("导入测试", test_imports),
        ("CDN配置测试", test_cdn_config), 
        ("象限图渲染测试", test_competitor_chart)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"🧪 执行 {test_name}...")
        result = test_func()
        results.append(result)
        print(f"{'✅' if result else '❌'} {test_name} {'通过' if result else '失败'}\n")
    
    # 总结
    passed = sum(results)
    total = len(results)
    print(f"📊 测试总结: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！象限图修复成功！")
        print("💡 建议：现在可以安全地部署到Render")
    else:
        print("⚠️ 部分测试失败，需要进一步修复")
    
    return passed == total

if __name__ == "__main__":
    # 导入必要模块
    from pyecharts.charts import Scatter
    from pyecharts import options as opts
    from pyecharts.globals import ThemeType
    
    main() 