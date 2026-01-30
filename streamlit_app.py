import streamlit as st
import requests

# 1. Cấu hình trang và ẨN THÔNG TIN (Menu, Footer, Header)
st.set_page_config(page_title="TikTok Downloader", page_icon="🎬")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #stDecoration {display:none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Giao diện chính
st.title("🎬 TikTok Video Downloader")
st.write("Dán link và tải video ngay lập tức.")

def get_download_link(tiktok_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {'url': tiktok_url, 'hd': 1}
    try:
        response = requests.post('https://www.tikwm.com/api/', data=data).json()
        if response.get('code') == 0:
            return response.get('data', {})
        return None
    except:
        return None

url_input = st.text_input("Nhập link TikTok:", placeholder="https://www.tiktok.com/...")

if url_input:
    with st.spinner('Đang xử lý...'):
        data = get_download_link(url_input)
        if data:
            video_url = data.get('hdplay') or data.get('play')
            if video_url and not video_url.startswith('http'):
                video_url = 'https://www.tikwm.com' + video_url
            
            st.success("Sẵn sàng tải về!")
            st.video(video_url)
            
            # Nút tải xuống
            video_bytes = requests.get(video_url).content
            st.download_button(
                label="📥 Bấm vào đây để lưu video",
                data=video_bytes,
                file_name="tiktok_no_watermark.mp4",
                mime="video/mp4",
                use_container_width=True # Nút to full màn hình điện thoại
            )
        else:
            st.error("Lỗi: Không tìm thấy video hoặc link sai.")
