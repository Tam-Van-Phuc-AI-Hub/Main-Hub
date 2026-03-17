import os
import time
from google import genai
import json

def market_scanner():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"❌ Lỗi API: {e}")
        return

    niches = ["Y tế cá nhân", "Giáo dục AI", "Tối ưu công việc", "Sức khỏe tâm thần", "Tài chính cá nhân", "Lofi Music"]
    
    # CHIẾN THUẬT GOM ĐƠN: 1 lần gọi AI cho tất cả ngách
    print(f"🔍 Đang quét tổng hợp cho {len(niches)} ngách (Tiết kiệm Quota)...")
    
    prompt = f"""Phân tích xu hướng 2026 cho các ngách: {', '.join(niches)}.
    Với mỗi ngách, hãy tìm 2 vấn đề lớn và 1 sản phẩm AI gợi ý từ Affitor.
    Trả về kết quả ngắn gọn cho từng ngách."""

    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        
        if response.text:
            # Lưu chung vào một file tổng để các bot khác tham khảo
            os.makedirs("projects", exist_ok=True)
            with open("projects/market_trends.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✅ Đã cập nhật xu hướng thị trường tổng hợp.")
            
    except Exception as e:
        if "429" in str(e):
            print("🚨 Cạn kiệt hạn ngạch ngày hôm nay rồi! Hãy nghỉ ngơi và quay lại sau 24h hoặc dùng Key mới.")
        else:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    market_scanner()
