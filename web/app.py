#!/usr/bin/env python3
"""
TradingAgents-CN Streamlit Web界面
基于Streamlit的股票分析Web应用程序
"""

import streamlit as st
import os
import sys
from pathlib import Path
import datetime
import time
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv(project_root / ".env", override=True)

# 导入自定义组件
from components.sidebar import render_sidebar
from components.header import render_header
from components.analysis_form import render_analysis_form
from components.results_display import render_results
# from utils.api_checker import check_api_keys  # 移除
from utils.analysis_runner import run_stock_analysis, validate_analysis_params, format_analysis_results
from utils.progress_tracker import StreamlitProgressDisplay, create_progress_callback

# 设置页面配置
st.set_page_config(
    page_title="TradingAgents-CN 股票分析平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/TauricResearch/TradingAgents',
        'Report a bug': 'https://github.com/TauricResearch/TradingAgents/issues',
        'About': """
        # TradingAgents-CN 股票分析平台
        
        基于多智能体大语言模型的中文金融交易决策框架
        
        **主要特性:**
        - 🤖 多智能体协作分析
        - 🇨🇳 中文优化的AI模型
        - 📊 实时股票数据分析
        - 🎯 专业投资建议
        
        **版本:** 1.0.0
        **开发团队:** TradingAgents-CN
        """
    }
)

# 自定义CSS样式
st.markdown('''
<style>
body {
    background: linear-gradient(135deg, #e3e9ef 0%, #bfc9d6 100%) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
/* 主内容最大宽度，居中显示 */
[data-testid="stHorizontalBlock"] > div:first-child {
    max-width: 1600px;
    margin-left: auto;
    margin-right: auto;
}
.glass-effect {
    position: relative;
    background: linear-gradient(120deg, rgba(220, 230, 245, 0.60) 0%, rgba(180, 200, 220, 0.38) 100%);
    backdrop-filter: blur(36px) saturate(180%) brightness(1.10);
    border: 1.8px solid rgba(180, 200, 220, 0.40);
    border-radius: 26px;
    box-shadow:
        0 8px 40px 0 rgba(120, 140, 180, 0.18),
        0 1.5px 8px 0 rgba(180, 200, 220, 0.10) inset,
        0 0.5px 0.5px 0 rgba(255,255,255,0.18) inset,
        0 0 32px 0 rgba(180,200,255,0.10) inset;
    padding: 2.5rem 2.5rem 2rem 2.5rem !important;
    margin-bottom: 2.5rem !important;
    overflow: hidden;
    transition: box-shadow 0.2s;
}
.glass-effect::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 22%;
    border-radius: 26px 26px 0 0;
    background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.08) 100%);
    pointer-events: none;
    z-index: 2;
}
.glass-effect::after {
    content: '';
    position: absolute;
    left: 0; right: 0; bottom: 0; height: 18%;
    border-radius: 0 0 26px 26px;
    background: linear-gradient(0deg, rgba(200,220,255,0.10) 0%, rgba(255,255,255,0.04) 100%);
    pointer-events: none;
    z-index: 2;
}
.glass-effect:hover {
    box-shadow: 0 14px 56px 0 rgba(120, 140, 180, 0.22), 0 2px 16px 0 rgba(180, 200, 220, 0.15) inset;
}
.button-glow, .stButton>button, .stDownloadButton>button {
    border-radius: 14px!important;
    font-weight: 600!important;
    background: linear-gradient(90deg, #e3e9ef 0%, #bfc9d6 100%)!important;
    color: #2a3340!important;
    border: 2px solid #e3e9ef!important;
    box-shadow: 0 2px 14px rgba(120,140,180,0.13)!important, 0 0.5px 0.5px 0 rgba(255,255,255,0.18) inset!important;
    padding: 0.8rem 1.8rem!important;
    transition: background 0.2s, box-shadow 0.2s;
}
.button-glow:hover, .stButton>button:hover, .stDownloadButton>button:hover {
    background: linear-gradient(90deg, #f5fafd 0%, #bfc9d6 100%)!important;
    box-shadow: 0 6px 22px rgba(120,140,180,0.18)!important, 0 1px 2px 0 rgba(255,255,255,0.22) inset!important;
}
input, select, textarea {
    background: linear-gradient(120deg, rgba(220,230,245,0.55) 0%, rgba(200,220,255,0.30) 100%)!important;
    border-radius: 12px!important;
    border: 2px solid #bfc9d6!important;
    box-shadow: 0 1.5px 8px rgba(180,200,220,0.13) inset!important, 0 0.5px 0.5px 0 rgba(255,255,255,0.13) inset!important;
    color: #2a3340!important;
}
.stTextInput>div>div>input, .stTextArea>div>textarea {
    background: linear-gradient(120deg, rgba(220,230,245,0.55) 0%, rgba(200,220,255,0.30) 100%)!important;
    color: #2a3340!important;
}
.stMetric, .stAlert, .stInfo, .stWarning, .stSuccess {
    background: rgba(220,230,245,0.38)!important;
    border-radius: 16px!important;
    color: #2a3340!important;
    border: 1.2px solid #bfc9d6!important;
    box-shadow: 0 1.5px 8px rgba(180,200,220,0.10) inset!important;
}
</style>
''', unsafe_allow_html=True)

# 隐藏Streamlit多页面导航
st.markdown("""
    <style>
    nav[data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    nav[data-testid="stSidebarNav"] * {display: none !important;}
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """初始化会话状态"""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analysis_running' not in st.session_state:
        st.session_state.analysis_running = False
    if 'last_analysis_time' not in st.session_state:
        st.session_state.last_analysis_time = None

def is_homepage():
    # 判断当前是否首页（股票分析页）
    # Streamlit 1.x: st.session_state.get('page', None) 可能不可用，采用URL路径判断
    return os.environ.get('ST_CUSTOM_PAGE', '') == ''

def main():
    """主应用程序"""

    # 初始化会话状态
    initialize_session_state()

    # 渲染页面头部
    render_header()

    # 页面导航
    # 删除所有 st.sidebar 相关的“选择功能”控件和标题

    # 默认显示股票分析页面
    # 渲染侧边栏
    config = render_sidebar()
    
    # 主内容区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 股票分析")
        
        # 渲染分析表单
        form_data = render_analysis_form()

        # 检查是否提交了表单
        if form_data.get('submitted', False):
            if not form_data['stock_symbol']:
                st.error("请输入股票代码")
            elif not form_data['analysts']:
                st.error("请至少选择一个分析师")
            else:
                # 执行分析
                st.session_state.analysis_running = True

                # 创建进度显示
                progress_container = st.container()
                progress_display = StreamlitProgressDisplay(progress_container)
                progress_callback = create_progress_callback(progress_display)

                try:
                    print(f"[DEBUG] config['api_key'] = {repr(config['api_key'])}, type = {type(config['api_key'])}")
                    results = run_stock_analysis(
                        stock_symbol=form_data['stock_symbol'],
                        analysis_date=form_data['analysis_date'],
                        analysts=form_data['analysts'],
                        research_depth=form_data['research_depth'],
                        llm_provider=config['llm_provider'],
                        market_type=form_data.get('market_type', '美股'),
                        llm_model=config['llm_model'],
                        progress_callback=progress_callback,
                        api_key=config['api_key'],
                        finnhub_api_key=config['finnhub_api_key']
                    )

                    # 清除进度显示
                    progress_display.clear()

                    # 格式化结果
                    formatted_results = format_analysis_results(results)

                    st.session_state.analysis_results = formatted_results
                    st.session_state.last_analysis_time = datetime.datetime.now()
                    st.success("✅ 分析完成！")

                except Exception as e:
                    # 清除进度显示
                    progress_display.clear()

                    st.error(f"❌ 分析失败: {str(e)}")
                    st.markdown("""
                    **可能的解决方案:**
                    1. 检查API密钥是否正确配置
                    2. 确认网络连接正常
                    3. 验证股票代码是否有效
                    4. 尝试减少研究深度或更换模型
                    """)
                finally:
                    st.session_state.analysis_running = False
        
        # 显示分析结果
        if st.session_state.analysis_results:
            render_results(st.session_state.analysis_results)
    
    with col2:
        # 使用指南卡片
        # st.markdown('<div class="glass-effect" style="padding:2.5rem; margin-bottom:2.5rem;">', unsafe_allow_html=True)
        st.header("ℹ️ 使用指南")
        with st.expander("🎯 快速开始", expanded=True):
            st.markdown("""
            1. **输入股票代码** (如 AAPL, TSLA, MSFT)
            2. **选择分析日期** (默认今天)
            3. **选择分析师团队** (至少一个)
            4. **设置研究深度** (1-5级)
            5. **点击开始分析**
            """)
        with st.expander("👥 分析师团队说明"):
            st.markdown("""
            - **📈 市场分析师**: 技术面分析，价格趋势
            - **💬 社交媒体分析师**: 投资者情绪分析
            - **📰 新闻分析师**: 新闻事件影响分析
            - **💰 基本面分析师**: 财务数据分析
            """)
        with st.expander("🧠 AI模型说明"):
            st.markdown("""
            - **Turbo**: 快速响应，适合快速查询
            - **Plus**: 平衡性能，推荐日常使用  
            - **Max**: 最强性能，适合深度分析
            """)
        st.markdown('</div>', unsafe_allow_html=True)
        # 风险提示卡片
        # st.markdown('<div class="glass-effect" style="padding:2.5rem; margin-bottom:2.5rem;">', unsafe_allow_html=True)
        st.header("💡 投资风险提示")
        st.markdown('''
        - 分析结果仅供参考，不构成投资建议
        - 投资有风险，入市需谨慎
        - 请结合多方信息进行决策
        - 重大投资建议咨询专业顾问
        ''')
        st.markdown('</div>', unsafe_allow_html=True)
        # TOKEN消费统计卡片
        # st.markdown('<div class="glass-effect" style="padding:2.5rem; margin-bottom:2.5rem;">', unsafe_allow_html=True)
        st.header("🔑 当前会话Token消耗统计")
        token_info = st.session_state.get('token_usage', None)
        if token_info:
            st.metric("总Token消耗", token_info.get('total_tokens', 0))
            st.metric("调用次数", token_info.get('call_count', 0))
            st.metric("累计费用(元)", token_info.get('total_cost', 0.0))
        else:
            st.info("暂无Token消耗数据。分析后将自动统计。")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 显示系统状态
        if st.session_state.last_analysis_time:
            st.info(f"🕒 上次分析时间: {st.session_state.last_analysis_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
