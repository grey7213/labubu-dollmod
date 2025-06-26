// ECharts 离线备用加载器
// 当CDN失败时自动降级到本地资源

(function() {
    'use strict';
    
    // 检查ECharts是否已加载
    function checkEChartsLoaded() {
        return typeof echarts !== 'undefined' && echarts.version;
    }
    
    // 如果ECharts未加载，尝试加载备用CDN
    if (!checkEChartsLoaded()) {
        console.log('🚨 主CDN加载失败，尝试备用CDN...');
        
        const fallbackCDNs = [
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
            };
            
            script.onerror = function() {
                console.warn(`⚠️ 备用CDN失败: ${fallbackCDNs[cdnIndex]}`);
                cdnIndex++;
                loadFallbackCDN();
            };
            
            document.head.appendChild(script);
        }
        
        // 延迟500ms后开始加载备用CDN
        setTimeout(loadFallbackCDN, 500);
    } else {
        console.log('✅ ECharts主CDN加载成功');
    }
    
    // 显示降级提示
    function showFallbackMessage() {
        const charts = document.querySelectorAll('iframe');
        charts.forEach(chart => {
            if (chart.src.includes('render_embed')) {
                chart.style.background = 'linear-gradient(135deg, #FFE4F1 0%, #E8F4FD 100%)';
                chart.style.display = 'flex';
                chart.style.alignItems = 'center';
                chart.style.justifyContent = 'center';
                chart.innerHTML = `
                    <div style="text-align: center; color: #2D3748; padding: 20px;">
                        <h3>📊 图表加载中...</h3>
                        <p>网络环境优化中，请稍后刷新页面</p>
                    </div>
                `;
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
            };
            
            iframe.onerror = function() {
                console.warn('⚠️ 图表iframe加载失败');
                this.style.background = 'linear-gradient(135deg, #FFE4F1 0%, #E8F4FD 100%)';
            };
        });
    });
    
})(); 