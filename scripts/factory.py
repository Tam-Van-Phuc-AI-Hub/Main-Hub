import os
import time
import re
from google import genai

def clean_html_only(raw_text):
    """Máy lọc siêu cấp: Chỉ lấy từ thẻ HTML mở đến thẻ HTML đóng"""
    # Tìm đoạn bắt đầu từ <!DOCTYPE hoặc <html và kết thúc bằng </html>
    pattern = re.compile(r'(<!DOCTYPE html>|<html.*?>).*?</html>', re.DOTALL | re.IGNORECASE)
    match = pattern.search(raw_text)
    
    if match:
        return match.group(0)
    
    # Nếu không tìm thấy thẻ chuẩn, lọc bỏ các dấu ``` của Markdown
    clean = re.sub(r'^```html\s*|^```\s*|```\s*$', '', raw_text, flags=re.MULTILINE)
    return clean.strip()

def factory_run():
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    aff_link = os.environ.get('AFFILIATE_LINK', '#')
    BRAND_NAME = "Tâm Vạn Phúc"
    project_root = "projects"
    
    if not os.path.exists(project_root): return

    folders = [f for f in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, f))]

    for folder in folders:
        path = os.path.join(project_root, folder)
        print(f"🏭 Đang sản xuất Landing Page cho: {folder}...")
        
        # Câu lệnh (Prompt) cực kỳ nghiêm khắc
        task = f"""Bạn là một máy xuất bản mã nguồn HTML.
        Nhiệm vụ: Thiết kế Landing Page cho ngách {folder} thuộc hệ sinh thái '{BRAND_NAME}'.
        Link Affiliate: {aff_link}
        YÊU CẦU BẮT BUỘC:
        - CHỈ trả về mã HTML/CSS/JS. 
        - TUYỆT ĐỐI KHÔNG có lời dẫn giải, KHÔNG chào hỏi, KHÔNG có văn bản bên ngoài thẻ <html>.
        - Phải có đầy đủ các thẻ <!DOCTYPE html>, <html>, <head>, <body>."""

        for attempt in range(3):
            try:
                response = client.models.generate_content(model='gemini-2.5-flash', contents=task)
                if response.text:
                    # Áp dụng máy lọc siêu cấp
                    final_code = clean_html_only(response.text)
                    
                    with open(f"{path}/index.html", "w", encoding="utf-8") as f:
                        f.write(final_code)
                    
                    print(f"✅ Đã dọn sạch và lưu file cho {folder}")
                    time.sleep(10)
                    break
            except Exception as e:
                print(f"⚠️ Đang thử lại {folder} do nghẽn mạng...")
                time.sleep(20)

if __name__ == "__main__":
    factory_run()
