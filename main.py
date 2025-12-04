from flask import Flask, render_template
import requests
import pandas as pd
import os # <--- ต้องมีบรรทัดนี้เพื่อแก้ NameError

# ----------------------------------------------
# --- 1. การตั้งค่าเริ่มต้นและการยืนยันตัวตน ---
# ----------------------------------------------

# สร้าง Flask Application
app = Flask(__name__)

# --- ฟังก์ชันดึงข้อมูล API (ต้องใช้ .ROBLOSECURITY Cookie) ---

def get_group_experiences(group_id, cookies):
    """ดึงรายการเกมทั้งหมดที่เป็นของกลุ่ม"""
    url = f"https://games.roblox.com/v2/groups/{group_id}/games?sortOrder=Desc&limit=100"
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        data = response.json()
        
        # กรองเอา PlaceId และ UniverseId
        games = [{'name': item['name'], 'universeId': item['id'], 'placeId': item['placeId']} 
                 for item in data.get('data', [])]
        return games
    except requests.RequestException:
        print(f"❌ Error ดึงเกมกลุ่ม {group_id} (อาจไม่มีเกมหรือ API มีปัญหา)")
        return []

def get_group_current_robux(group_id, cookies):
    """ดึงยอด Robux คงเหลือปัจจุบันของกลุ่ม (ต้องใช้สิทธิ์)"""
    url = f"https://economy.roblox.com/v1/groups/{group_id}/currency"
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        data = response.json()
        
        # ตรวจสอบว่ามีข้อมูล Robux และ return
        if data.get('robux'):
            # Format ตัวเลข Robux เป็นสตริงที่มี comma คั่น
            return f"R$ {data['robux']:,.0f}" 
        return "R$ 0"
    except requests.RequestException as e:
        print(f"❌ Error ดึงยอด Robux กลุ่ม {group_id}: {e}")
        return "N/A (ตรวจสอบสิทธิ์)"


def get_game_revenue_stats(universe_id, cookies):
    """ดึงข้อมูล Revenue ของเกม (ต้องใช้สิทธิ์)"""
    # NOTE: API สำหรับสถิติ Developer มักต้องใช้เวลาและมีการตั้งค่าซับซ้อน
    # เราจะใช้ API ตัวอย่างนี้และจำกัดการแสดงผลเพื่อสาธิต
    end_date = pd.Timestamp.now(tz='UTC')
    start_date = end_date - pd.Timedelta(days=30)
    
    # ดึงรายได้ 30 วันย้อนหลัง (ตัวอย่าง)
    url = (f"https://develop.roblox.com/v1/places/{universe_id}/stats/Revenue"
           f"?granularity=Daily&startTime={start_date.isoformat()}&endTime={end_date.isoformat()}")

    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            total_revenue = df['value'].sum()
            return f"R$ {total_revenue:,.0f}"
        return "R$ 0"
    
    except requests.RequestException as e:
        # 403 Forbidden มักหมายถึงไม่มีสิทธิ์
        return "N/A (ไม่มีสิทธิ์/API)"


# ------------------------------------------
# --- 2. ฟังก์ชันรวมการวิเคราะห์ข้อมูล ---
# ------------------------------------------

def fetch_and_analyze_data():
    """ฟังก์ชันรวมการดึงและวิเคราะห์ข้อมูลสำหรับทุกกลุ่ม"""
    # โหลด Environment Variables
    ROBLOX_COOKIE = os.getenv("ROBLOX_COOKIE")
    GROUP_IDS = [int(g) for g in os.getenv("GROUP_IDS", "").split(',') if g.isdigit()]
    
    if not ROBLOX_COOKIE:
        return [{'group_name': 'Error', 'group_id': '0', 'current_robux': '❌ กรุณาตั้งค่า ROBLOX_COOKIE', 'games_data': []}]

    COOKIES = {'.ROBLOSECURITY': ROBLOX_COOKIE}
    
    # รายชื่อกลุ่มสำหรับตั้งชื่อ (สามารถดึงชื่อจริงจาก API ได้ถ้าต้องการ)
    GROUP_NAMES = {
        35507841: "Gn-Studios",
        6443807: "Nearo"
    }
    
    analysis_results = []
    
    for group_id in GROUP_IDS:
        group_name = GROUP_NAMES.get(group_id, f"Group {group_id}")
        
        # 1. ดึงรายการเกม
        games = get_group_experiences(group_id, COOKIES) 
        
        # 2. ดึงข้อมูลทางการเงินกลุ่ม
        current_robux = get_group_current_robux(group_id, COOKIES)
        
        group_revenue_data = {
            'group_id': group_id,
            'group_name': group_name,
            'current_robux': current_robux,
            'games_data': []
        }
        
        # 3. ดึงข้อมูลรายได้เกมแต่ละเกม
        for game in games:
            # ดึงรายได้เกม
            total_revenue = get_game_revenue_stats(game['universeId'], COOKIES) 
            game['total_revenue'] = total_revenue
            group_revenue_data['games_data'].append(game)
            
        analysis_results.append(group_revenue_data)

    return analysis_results

# ------------------------------------------
# --- 3. Flask Route ---
# ------------------------------------------

@app.route('/')
def index():
    """Route หลักสำหรับแสดงผล Dashboard"""
    # เรียกใช้ฟังก์ชันวิเคราะห์เพื่อดึงข้อมูลทั้งหมด
    data = fetch_and_analyze_data()
    
    # ส่งข้อมูลที่วิเคราะห์แล้วไปยังไฟล์ index.html
    return render_template('index.html', analysis_data=data)

if __name__ == '__main__':
    # การตั้งค่าพอร์ตสำหรับ Render.com
    port = int(os.environ.get("PORT", 5000))
    # ตั้ง host เป็น 0.0.0.0 เพื่อให้ Render เข้าถึงได้
    app.run(host='0.0.0.0', port=port)
