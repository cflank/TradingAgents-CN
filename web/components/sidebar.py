"""
侧边栏组件
"""

import streamlit as st
import os

def render_sidebar():
    """
    渲染侧边栏配置
    """
    with st.sidebar:
        st.header("🔧 系统配置")

        # LLM提供商选择
        llm_provider = st.selectbox(
            "选择LLM提供商",
            options=["dashscope", "google", "openai"],
            index=0,
            format_func=lambda x: {
                "dashscope": "阿里百炼 - 国产模型",
                "google": "Google AI - Gemini模型",
                "openai": "OpenAI - GPT模型"
            }[x],
            help="选择AI模型提供商"
        )

        # 根据提供商显示不同的模型
        if llm_provider == "dashscope":
            llm_model = st.selectbox(
                "选择阿里百炼模型",
                options=["qwen-turbo", "qwen-plus-latest", "qwen-max"],
                index=1,
                format_func=lambda x: {
                    "qwen-turbo": "通义千问 Turbo - 快速响应",
                    "qwen-plus-latest": "通义千问 Plus - 平衡性能",
                    "qwen-max": "通义千问 Max - 最强性能"
                }[x],
                help="选择用于分析的阿里百炼模型"
            )
            api_key_label = "阿里百炼 API Key"
            api_key_key = "dashscope_api_key"
        elif llm_provider == "google":
            llm_model = st.selectbox(
                "选择Google模型",
                options=["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
                index=0,
                format_func=lambda x: {
                    "gemini-2.0-flash": "Gemini 2.0 Flash - 推荐使用",
                    "gemini-1.5-pro": "Gemini 1.5 Pro - 强大性能",
                    "gemini-1.5-flash": "Gemini 1.5 Flash - 快速响应"
                }[x],
                help="选择用于分析的Google Gemini模型"
            )
            api_key_label = "Google API Key"
            api_key_key = "google_api_key"
        else:  # openai
            llm_model = st.selectbox(
                "选择OpenAI模型",
                options=["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
                index=1,
                format_func=lambda x: {
                    "gpt-3.5-turbo": "GPT-3.5 Turbo",
                    "gpt-4": "GPT-4",
                    "gpt-4o": "GPT-4o (多模态)"
                }[x],
                help="选择用于分析的OpenAI模型"
            )
            api_key_label = "OpenAI API Key"
            api_key_key = "openai_api_key"

        # API Key输入框，失焦时校验
        def api_key_on_blur():
            key = st.session_state.get(api_key_key, "")
            if not key or len(key) < 10:
                st.session_state[f"{api_key_key}_status"] = (False, "API Key 格式无效")
            else:
                st.session_state[f"{api_key_key}_status"] = (True, "API Key 格式有效")

        api_key = st.text_input(
            api_key_label,
            value=st.session_state.get(api_key_key, ""),
            type="password",
            key=api_key_key,
            on_change=api_key_on_blur
        )
        status = st.session_state.get(f"{api_key_key}_status", (None, ""))
        if status[0] is True:
            st.success(f"✅ {api_key_label} 已设置")
        elif status[0] is False:
            st.error(f"❌ {api_key_label} 无效: {status[1]}")
        else:
            st.info(f"请输入{api_key_label}")

        # FinnHub API Key 输入框（始终显示，必填）
        def finnhub_key_on_blur():
            key = st.session_state.get('finnhub_api_key', "")
            if not key or len(key) < 10:
                st.session_state['finnhub_api_key_status'] = (False, "API Key 格式无效")
            else:
                st.session_state['finnhub_api_key_status'] = (True, "API Key 格式有效")

        finnhub_api_key = st.text_input(
            "FinnHub API Key (必填)",
            value=st.session_state.get('finnhub_api_key', ""),
            type="password",
            key='finnhub_api_key',
            on_change=finnhub_key_on_blur
        )
        finnhub_status = st.session_state.get('finnhub_api_key_status', (None, ""))
        if finnhub_status[0] is True:
            st.success("✅ FinnHub API Key 已设置")
        elif finnhub_status[0] is False:
            st.error(f"❌ FinnHub API Key 无效: {finnhub_status[1]}")
        else:
            st.info("请输入FinnHub API Key")

        st.markdown("---")

        # AI模型配置
        st.subheader("🧠 AI模型配置")

        # 高级设置
        with st.expander("⚙️ 高级设置"):
            enable_memory = st.checkbox(
                "启用记忆功能",
                value=False,
                help="启用智能体记忆功能（可能影响性能）"
            )
            
            enable_debug = st.checkbox(
                "调试模式",
                value=False,
                help="启用详细的调试信息输出"
            )
            
            max_tokens = st.slider(
                "最大输出长度",
                min_value=1000,
                max_value=8000,
                value=4000,
                step=500,
                help="AI模型的最大输出token数量"
            )
        
        st.markdown("---")
        
        # 系统信息
        st.subheader("ℹ️ 系统信息")
        
        st.info("""
        **版本**: 1.0.0
        **框架**: Streamlit + LangGraph
        **数据源**: FinnHub API
        """)
        
        # 帮助链接
        st.subheader("📚 帮助资源")
        
        st.markdown("""
        - [📖 使用文档](https://github.com/TauricResearch/TradingAgents)
        - [🐛 问题反馈](https://github.com/TauricResearch/TradingAgents/issues)
        - [💬 讨论社区](https://github.com/TauricResearch/TradingAgents/discussions)
        - [🔑 API密钥配置](../docs/security/api_keys_security.md)
        """)
    
    # 返回所有配置信息
    return {
        'llm_provider': llm_provider,
        'llm_model': llm_model,
        'enable_memory': enable_memory,
        'enable_debug': enable_debug,
        'max_tokens': max_tokens,
        'api_key': api_key,
        'api_key_key': api_key_key,
        'finnhub_api_key': finnhub_api_key
    }
