import streamlit as st
import requests

# ==========================================
# 🎨 CẤU HÌNH GIAO DIỆN & ẨN THÔNG TIN THỪA
# ==========================================
st.set_page_config(
    page_title="Tải Video TikTok",
    page_icon="🎬",
    layout="centered"
)

# CSS để xóa sạch Header đỏ, nút Deploy và Footer
hide_st_style = """
            <style>
            header {visibility: hidden !important;}
            .stAppDeployButton {display:none !important;}
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            #stDecoration {display:none !important;}
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# 🛠️ HÀM XỬ LÝ LẤY LINK VIDEO (API)
# ==========================================
def get_tiktok_data(url):
    api_url = "https://www.tikwm.com/api/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
    }
    params = {"url": url, "hd": 1}
    
    try:
        response = requests.post(api_url, headers=headers, data=params)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# ==========================================
# 📱 GIAO DIỆN NGƯỜI DÙNG
# ==========================================
st.title("🚀 TikTok Downloader")
st.write("Tải video TikTok không logo, chất lượng cao nhất.")

# Ô nhập link
link = st.text_input("Dán link video TikTok vào đây:", placeholder="https://www.tiktok.com/@user/video/...")

if link:
    with st.spinner('Đang lấy dữ liệu video...'):
        result = get_tiktok_data(link)
        
        if result and result.get('code') == 0:
            data = result.get('data', {})
            # Lấy link HD nếu có, không thì lấy link thường
            video_url = data.get('hdplay') or data.get('play')
            
            # Sửa lỗi link thiếu giao thức https
            if video_url and not video_url.startswith('http'):
                video_url = 'https://www.tikwm.com' + video_url

            if video_url:
                st.success("✅ Đã tìm thấy video!")
                
                # Hiển thị video để xem trước
                st.video(video_url)
                
                # Xử lý nút tải về
                try:
                    video_bytes = requests.get(video_url).content
                    st.download_button(
                        label="📥 BẤM VÀO ĐÂY ĐỂ TẢI VIDEO",
                        data=video_bytes,
                        file_name="tiktok_video.mp4",
                        mime="video/mp4",
                        use_container_width=True # Nút rộng hết cỡ cho điện thoại
                    )
                except:
                    st.error("Không thể tải dữ liệu video về server. Vui lòng thử lại.")
            else:
                st.error("Không tìm thấy link tải video.")
        else:
            st.error("Link không hợp lệ hoặc video đã bị xóa.")

st.info("💡 Mẹo: Nhấn vào dấu 3 chấm trên video để chọn 'Tải xuống' nếu nút bấm không hoạt động.")
