import os
from google import genai
import re

def factory_run():
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    aff_link = os.environ.get('AFFILIATE_LINK', '#')
    
    # Quét qua tất cả các thư mục trong /projects
    project_root = "projects"
    for folder in os.listdir(project_root):
        path = os.path.join(project_root, folder)
        if os.path.isdir(path):
            print(f"🏭 Đang sản xuất Landing Page cho: {folder}")
            
            # Câu lệnh yêu cầu AI thiết kế dựa trên ngách cụ thể
            task = f"Viết mã HTML/CSS Landing Page chuyên nghiệp cho ngách {folder}. Mục tiêu: Affiliate sản phẩm AI từ Affitor. Link: {aff_link}. Giao diện Glassmorphism, phong cách hiện đại 2026."
            
            response = client.models.generate_content(model='gemini-2.5-flash', contents=task)
            
            if response.text:
                # Làm sạch và lưu vào file index.html của từng ngách
                clean_html = re.sub(r'^```html\s*|^```\s*|```\s*$', '', response.text, flags=re.MULTILINE)
                with open(f"{path}/index.html", "w", encoding="utf-8") as f:
                    f.write(clean_html.strip())

if __name__ == "__main__":
    factory_run()
