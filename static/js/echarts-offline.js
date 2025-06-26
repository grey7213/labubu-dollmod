// ECharts 离线备用加载器 - 云端优化版
// 当CDN失败时自动降级到本地资源

(function() {
    'use strict';
    
    // 检查ECharts是否已加载
    function checkEChartsLoaded() {
        return typeof echarts !== 'undefined' && echarts.version;
    }
    
    // 检测环境类型
    function isProductionEnvironment() {
        const hostname = window.location.hostname;
        return hostname.includes('render.com') || 
               hostname.includes('herokuapp.com') || 
               hostname.includes('onrender.com') ||
               !hostname.includes('localhost') && !hostname.includes('127.0.0.1');
    }
    
    // 如果ECharts未加载，尝试加载备用CDN
    if (!checkEChartsLoaded()) {
        console.log('🚨 主CDN加载失败，尝试备用CDN...');
        
        // 根据环境选择不同的CDN策略
        const isProd = isProductionEnvironment();
        const fallbackCDNs = isProd ? [
            // 生产环境：优先选择稳定性高的CDN
            'https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js',
            'https://unpkg.com/echarts@5.4.3/dist/echarts.min.js',
            'https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js',
            'https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js'
        ] : [
            // 开发环境：使用原有策略
            'https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js',
            'https://unpkg.com/echarts@5.4.3/dist/echarts.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js'
        ];
        
        let cdnIndex = 0;
        
        function loadFallbackCDN() {
            if (cdnIndex >= fallbackCDNs.length) {
                console.error('❌ 所有ECharts CDN都加载失败');
                showFallbackMessage();
                return;
            }
            
            const script = document.createElement('script');
            script.src = fallbackCDNs[cdnIndex];
            script.async = true;
            
            script.onload = function() {
                console.log(`✅ 备用CDN加载成功: ${fallbackCDNs[cdnIndex]}`);
                // 通知页面ECharts已可用
                document.dispatchEvent(new CustomEvent('echartsLoaded'));
                // 尝试重新渲染失败的图表
                retryFailedCharts();
            };
            
            script.onerror = function() {
                console.warn(`⚠️ 备用CDN失败: ${fallbackCDNs[cdnIndex]}`);
                cdnIndex++;
                setTimeout(loadFallbackCDN, 500); // 延迟500ms重试
            };
            
            document.head.appendChild(script);
        }
        
        // 延迟后开始加载备用CDN
        const retryDelay = isProd ? 1000 : 500; // 生产环境延迟更长
        setTimeout(loadFallbackCDN, retryDelay);
    } else {
        console.log('✅ ECharts主CDN加载成功');
    }
    
    // 重试失败的图表
    function retryFailedCharts() {
        const charts = document.querySelectorAll('iframe, .chart-container');
        charts.forEach(chart => {
            if (chart.dataset && chart.dataset.retry === 'pending') {
                console.log('🔄 重试渲染图表...');
                // 触发图表重新渲染
                if (chart.contentWindow && chart.contentWindow.location) {
                    chart.contentWindow.location.reload();
                }
            }
        });
    }
    
    // 显示降级提示
    function showFallbackMessage() {
        const charts = document.querySelectorAll('iframe[src*="chart"], .chart-container');
        charts.forEach(chart => {
            // 创建备用显示内容
            const fallbackDiv = document.createElement('div');
            fallbackDiv.style.cssText = `
                width: 100%; 
                height: 500px; 
                background: linear-gradient(135deg, #FFE4F1 0%, #E8F4FD 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: #2D3748;
                font-family: 'Microsoft YaHei', sans-serif;
            `;
            
            fallbackDiv.innerHTML = `
                <div>
                    <h3 style="margin: 0 0 15px 0;">📊 图表加载中...</h3>
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        网络环境优化中，请稍后刷新页面或检查网络连接
                    </p>
                    <button onclick="window.location.reload()" 
                            style="margin-top: 15px; padding: 8px 16px; 
                                   background: #FF6B9D; color: white; border: none; 
                                   border-radius: 4px; cursor: pointer;">
                        刷新页面
                    </button>
                </div>
            `;
            
            // 替换原有内容
            if (chart.parentNode) {
                chart.parentNode.insertBefore(fallbackDiv, chart);
                chart.style.display = 'none';
            }
        });
    }
    
    // 图表容器优化
    document.addEventListener('DOMContentLoaded', function() {
        const iframes = document.querySelectorAll('iframe');
        iframes.forEach(iframe => {
            iframe.style.minHeight = '500px';
            iframe.style.background = 'transparent';
            
            // 监听iframe加载
            iframe.onload = function() {
                console.log('📊 图表iframe加载完成');
                this.dataset.retry = 'success';
            };
            
            iframe.onerror = function() {
                console.warn('⚠️ 图表iframe加载失败');
                this.dataset.retry = 'pending';
                this.style.background = 'linear-gradient(135deg, #FFE4F1 0%, #E8F4FD 100%)';
            };
        });
        
        // 监听网络状态变化
        if (navigator.onLine !== undefined) {
            window.addEventListener('online', function() {
                console.log('🌐 网络连接恢复，尝试重新加载图表');
                setTimeout(() => {
                    if (!checkEChartsLoaded()) {
                        window.location.reload();
                    }
                }, 1000);
            });
            
            window.addEventListener('offline', function() {
                console.warn('📡 网络连接断开');
            });
        }
    });
    
    // 页面可见性变化时检查图表状态
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && !checkEChartsLoaded()) {
            console.log('👁️ 页面重新可见，检查ECharts状态...');
            setTimeout(() => {
                if (!checkEChartsLoaded()) {
                    console.log('🔄 尝试重新加载ECharts...');
                    window.location.reload();
                }
            }, 2000);
        }
    });
    
})(); 