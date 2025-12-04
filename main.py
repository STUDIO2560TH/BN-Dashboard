from flask import Flask, render_template
import requests
import os 
import pandas as pd # ยังคงเก็บไว้เผื่อใช้ในการวิเคราะห์ข้อมูลอื่น ๆ

# ----------------------------------------------
# --- 1. การตั้งค่าเริ่มต้นและ API สาธารณะ ---
# ----------------------------------------------

# สร้าง Flask Application
app = Flask(__name__)

# --- ฟังก์ชันดึงข้อมูล API สาธารณะ ---

def get_group_experiences(group_id):
    """ดึงรายการเกมทั้งหมดที่เป็นของกลุ่ม (Public API)"""
    url = f"https://games.roblox.com/v2/groups/{group_id}/games?sortOrder=Desc&limit=100"
    try:
        response = requests.get(url) 
        response.raise_for_status()
        data = response.json()
        
        # กรองเอา PlaceId และ UniverseId และแก้ไข KeyError ด้วย .get()
        games = [{'name': item['name'], 
                  'universeId': item.get('id'), 
                  'placeId': item.get('placeId')} 
                 for item in data.get('data', []) if item.get('id') is not None]
        return games
    except requests.RequestException:
        print(f"❌ Error ดึงเกมกลุ่ม {group_id} (อาจไม่มีเกมหรือ API มีปัญหา)")
        return []

def get_game_player_counts(universe_ids):
    """ดึงจำนวนผู้เล่นปัจจุบันของเกมจาก Universe ID หลายตัว (Public API)"""
    universe_id_list = [str(uid) for uid in universe_ids if uid is not None]
    if not universe_id_list:
        return {}
        
    # API สำหรับดึงสถิติผู้เล่นปัจจุบัน
    url = "https://games.roblox.com/v1/games?"
    params = {'universeIds': universe_id_list}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # จัดรูปแบบผลลัพธ์เป็น Dictionary: {universeId: currentPlayers}
        player_counts = {item['id']: item.get('playing', 0) 
                         for item in data.get('data', [])}
        return player_counts
    except requests.RequestException as e:
        print(f"❌ Error ดึงจำนวนผู้เล่น: {e}")
        return {}

# ------------------------------------------
# --- 2. ฟังก์ชันรวมการวิเคราะห์ข้อมูล ---
# ------------------------------------------

def fetch_and_analyze_data():
    """ฟังก์ชันรวมการดึงและวิเคราะห์ข้อมูลผู้เล่นสำหรับทุกกลุ่ม"""
    # ดึง GROUP_IDS เท่านั้น ไม่ใช้ ROBLOX_COOKIE
    GROUP_IDS = [int(g) for g in os.getenv("GROUP_IDS", "").split(',') if g.isdigit()]
    
    if not GROUP_IDS:
        return [{'group_name': 'Error', 'group_id': '0', 'total_players_summary': '❌ กรุณาตั้งค่า GROUP_IDS ใน Environment Variables', 'games_data': []}]

    GROUP_NAMES = {
        35507841: "Gn-Studios",
        6443807: "Nearo"
    }
    
    group_games_map = {}
    all_universe_ids = []
    
    # Phase 1: ดึงรายชื่อเกมทั้งหมดเพื่อรวบรวม Universe IDs
    for group_id in GROUP_IDS:
        group_name = GROUP_NAMES.get(group_id, f"Group {group_id}")
        games = get_group_experiences(group_id) 
        
        group_games_map[group_id] = {
            'group_name': group_name,
            'group_id': group_id,
            'games_data': games
        }
        all_universe_ids.extend([game['universeId'] for game in games])

    # Phase 2: ดึงจำนวนผู้เล่นทั้งหมดในครั้งเดียว
    player_counts = get_game_player_counts(all_universe_ids)

    # Phase 3: ผสานข้อมูลและสรุปผล
    analysis_results = []
    for group_id, group_data in group_games_map.items():
        total_players = 0
        for game in group_data['games_data']:
            uid = game['universeId']
            # เพิ่มจำนวนผู้เล่นลงในข้อมูลเกม
            game['current_players'] = player_counts.get(uid, 0)
            total_players += game['current_players']
            
        group_data['total_players_summary'] = f"{total_players:,}"
        analysis_results.append(group_data)

    return analysis_results

# ------------------------------------------
# --- 3. Flask Route ---
# ------------------------------------------

@app.route('/')
def index():
    """Route หลักสำหรับแสดงผล Dashboard"""
    data = fetch_and_analyze_data()
    
    # ส่งข้อมูลที่วิเคราะห์แล้วไปยังไฟล์ index.html
    return render_template('index.html', analysis_data=data)

if __name__ == '__main__':
    # การตั้งค่าพอร์ตสำหรับ Render.com
    port = int(os.environ.get("PORT", 5000))
    # ตั้ง host เป็น 0.0.0.0 เพื่อให้ Render เข้าถึงได้
    app.run(host='0.0.0.0', port=port)
