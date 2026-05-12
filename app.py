import streamlit as st
import google.generativeai as genai

# --- 頁面基本配置 ---
st.set_page_config(page_title="Gemini API 測試", page_icon="🤖")

def init_gemini():
    """初始化 Gemini API 配置"""
    try:
        # 從 Streamlit Secrets 讀取金鑰
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-3.0-flash')
    except Exception as e:
        st.error(f"❌ 金鑰設定錯誤: {e}")
        st.info("請確保在 .streamlit/secrets.toml 或 Streamlit Cloud 後台已設定 GEMINI_API_KEY")
        st.stop()

def main():
    # 1. 標題與說明
    st.title("🤖 Gemini API 連線測試")
    st.caption("這是一個簡單的連線測試工具，確保您的環境配置正確。")
    
    # 2. 初始化模型
    model = init_gemini()

    # 3. 提示資訊
    with st.expander("📌 使用說明", expanded=True):
        st.info("若能成功收到 AI 回覆，表示您的 GitHub 與 Secrets 環境配置正確！")

    # 4. 簡單輸入介面 (改用 st.chat_input 更有對話感)
    user_input = st.chat_input("輸入一段話測試連線 (例如: 你好)...")

    if user_input:
        # 顯示使用者的輸入
        with st.chat_message("user"):
            st.write(user_input)

        # 呼叫 API 並顯示回覆
        with st.chat_message("assistant"):
            with st.spinner("AI 正在思考中..."):
                try:
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                    st.success("✅ 連線成功！")
                except Exception as e:
                    st.error(f"❌ 呼叫 API 失敗: {e}")

if __name__ == "__main__":
    main()
