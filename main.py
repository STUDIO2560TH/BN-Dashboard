from flask import Flask, render_template
import requests
import pandas as pd
import os
from dotenv import load_dotenv
# นำเข้าฟังก์ชันการวิเคราะห์ (get_group_experiences, get_group_transactions, etc.) จากโค้ดเดิม
# ... (วางโค้ดฟังก์ชันการดึงข้อมูล API จากคำตอบก่อนหน้าไว้ที่นี่) ...

# สร้าง Flask Application
app = Flask(__name__)

# --- ฟังก์ชันรวมการวิเคราะห์ข้อมูล ---
# (นำโค้ด run_analysis เดิมมาปรับให้ return ข้อมูลแทนการ print)
def fetch_and_analyze_data():
    load_dotenv()
    ROBLOX_COOKIE = os.getenv("ROBLOX_COOKIE")
    GROUP_IDS = [int(g) for g in os.getenv("GROUP_IDS", "").split(',') if g.isdigit()]

    # ... (โค้ดตรวจสอบ Cookie/ID และ COOKIES/HEADERS dictionaries) ...
    
    analysis_results = []
    
    for group_id in GROUP_IDS:
        # 1. ดึงรายการเกม
        games = get_group_experiences(group_id) 
        
        # 2. ดึงข้อมูลทางการเงินกลุ่ม (สมมติว่าคุณมีฟังก์ชันที่ return ยอดคงเหลือได้)
        # NOTE: ในตัวอย่างนี้จะใช้ค่าคงที่แทน เพราะฟังก์ชันเดิมแค่ print
        group_revenue_data = {
            'group_id': group_id,
            'group_name': "Gn-Studios" if group_id == 35507841 else "Nearo",
            'current_robux': f"R$ {group_id * 1000}", # <--- แทนที่ด้วยยอดจริงที่ดึงจาก API
            'games_data': []
        }
        
        # 3. ดึงข้อมูลรายได้เกม
        for game in games:
            # ดึงรายได้เกม (เรียก get_game_revenue_stats) 
            # ...
            # game['total_revenue'] = get_game_revenue_stats(game['universeId']) 
            game['total_revenue'] = f"R$ {game['universeId'] % 10000}" # <--- แทนที่ด้วยยอดจริง
            group_revenue_data['games_data'].append(game)
            
        analysis_results.append(group_revenue_data)

    return analysis_results

# --- Flask Route สำหรับแสดงผลหน้าหลัก ---
@app.route('/')
def index():
    # เรียกใช้ฟังก์ชันวิเคราะห์เพื่อดึงข้อมูลทั้งหมด
    data = fetch_and_analyze_data()
    
    # ส่งข้อมูลที่วิเคราะห์แล้วไปยังไฟล์ index.html
    return render_template('index.html', analysis_data=data)

if __name__ == '__main__':
    # การตั้งค่าพอร์ตสำหรับ Render.com
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
