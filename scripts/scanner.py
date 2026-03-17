import os
from google import genai

def market_scanner():
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    
    # Danh sách 6 ngách chiến lược
    niches = ["Y tế cá nhân", "Giáo dục AI", "Tối ưu công việc", "Sức khỏe tâm thần", "Tài chính cá nhân"]
    
    for niche in niches:
        print(f"🔍 Đang quét 100 nguồn dữ liệu cho ngách: {niche}...")
        
        # Lệnh để AI phân tích xu hướng và tìm sản phẩm trên Affitor
        prompt = f"""Phân tích 100 kênh nội dung (YouTube, Blog, Forum) hàng đầu về {niche}.
        1. Tìm ra 3 vấn đề (Pain Points) lớn nhất người dùng đang gặp phải năm 2026.
        2. Đề xuất sản phẩm AI phù hợp nhất từ https://list.affitor.com/programs để giải quyết vấn đề đó.
        3. Trả về định dạng JSON để nạp vào hệ thống tự động."""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Lưu dữ liệu thô vào thư mục dự án tương ứng
        folder = f"projects/{niche.lower().replace(' ', '-')}"
        os.makedirs(folder, exist_ok=True)
        with open(f"{folder}/market_data.json", "w", encoding="utf-8") as f:
            f.write(response.text)
            
    print("✅ Đã hoàn thành quét thị trường cho tất cả các ngách.")

if __name__ == "__main__":
    market_scanner()
