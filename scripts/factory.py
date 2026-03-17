import os
import time
from google import genai
import re
import sys

def factory_run():
    # Khởi tạo client
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"❌ Lỗi khởi tạo API: {e}")
        return

    BRAND_NAME = "Tâm Vạn Phúc"
    project_root = "projects"
    
    # Lấy danh sách các thư mục dự án
    folders = [f for f in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, f))]

    for folder in folders:
        path = os.path.join(project_root, folder)
        print(f"🏭 Đang xử lý ngách: {folder}...")

        task = f"""Bạn là chuyên gia thiết kế Landing Page cho hệ sinh thái '{BRAND_NAME}'.
        Sản phẩm: Các công cụ AI hỗ trợ {folder} lấy từ Affitor.
        YÊU CẦU:
        1. Tone & Mood: Chân thành, nhân văn, hiện đại (Style: Clean & Minimalist).
        2. CTA: Gắn link {os.environ.get('AFFILIATE_LINK', '#')} vào các nút bấm nổi bật.
        3. Footer: 'Bản quyền thuộc về {BRAND_NAME} AI Hub - Công nghệ vì cuộc sống hạnh phúc.'
        4. Trả về mã HTML/CSS hoàn chỉnh trong 1 file."""

        # CƠ CHẾ THỬ LẠI (RETRY LOGIC)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(model='gemini-2.5-flash', contents=task)
                
                if response.text:
                    clean_html = re.sub(r'^```html\s*|^```\s*|```\s*$', '', response.text, flags=re.MULTILINE)
                    with open(f"{path}/index.html", "w", encoding="utf-8") as f:
                        f.write(clean_html.strip())
                    print(f"✅ Đã tạo xong Landing Page cho {folder}")
                    
                    # NGHỈ NGƠI 10 GIÂY giữa các lần gọi để tránh quá tải
                    print("☕ Nghỉ 10 giây để Google bớt 'căng thẳng'...")
                    time.sleep(10)
                    break # Thành công thì thoát vòng lặp thử lại
            
            except Exception as e:
                if "503" in str(e) or "429" in str(e):
                    wait_time = (attempt + 1) * 20 # Đợi lâu hơn sau mỗi lần lỗi
                    print(f"⚠️ Google đang bận (Lần {attempt+1}). Thử lại sau {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Lỗi không xác định tại {folder}: {e}")
                    break

if __name__ == "__main__":
    factory_run()
