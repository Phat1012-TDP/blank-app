import streamlit as st
import requests
import os

st.set_page_config(page_title="TikTok Downloader", page_icon="🎬")

st.title("🎬 TikTok Downloader (No Watermark)")
st.caption("Dán link TikTok vào bên dưới để tải video chất lượng cao.")

# Hàm xử lý tải (chỉnh sửa từ code của bạn)
def get_download_link(tiktok_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {'url': tiktok_url, 'hd': 1}
    try:
        response = requests.post('https://www.tikwm.com/api/', data=data).json()
        if response.get('code') == 0:
            data_video = response.get('data', {})
            download_url = data_video.get('hdplay') or data_video.get('play')
            if download_url and not download_url.startswith('http'):
                download_url = 'https://www.tikwm.com' + download_url
            return download_url
        return None
    except:
        return None

# Giao diện người dùng
url_input = st.text_input("Nhập link TikTok:", placeholder="https://www.tiktok.com/@user/video/...")

if url_input:
    with st.spinner('Đang lấy link video...'):
        video_link = get_download_link(url_input)
        
        if video_link:
            st.success("Đã tìm thấy video!")
            # Nút tải về trực tiếp cho điện thoại
            st.video(video_link)
            
            # Nút Download
            video_data = requests.get(video_link).content
            st.download_button(
                label="📥 Tải video về máy",
                data=video_data,
                file_name="tiktok_video.mp4",
                mime="video/mp4"
            )
        else:
            st.error("Không thể lấy link video. Vui lòng kiểm tra lại URL.")
