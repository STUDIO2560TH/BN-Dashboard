import requests
import pandas as pd
import os
from dotenv import load_dotenv

# โหลด .env สำหรับการทดสอบ Local (Render จะใช้ Environment Variables โดยตรง)
load_dotenv()

# --- 1. การตั้งค่า ---
ROBLOX_COOKIE = os.getenv("ROBLOX_COOKIE")
GROUP_IDS = [int(g) for g in os.getenv("GROUP_IDS", "").split(',') if g.isdigit()]

if not ROBLOX_COOKIE or not GROUP_IDS:
    print("❌ Error: ต้องตั้งค่า ROBLOX_COOKIE และ GROUP_IDS")
    exit()

# Headers สำหรับการยืนยันตัวตน (Authentication)
COOKIES = {'.ROBLOSECURITY': ROBLOX_COOKIE}
HEADERS = {'X-CSRF-TOKEN': 'fetch'} # ใช้เพื่อดึง CSRF token ก่อน (สำคัญสำหรับการส่ง POST/PUT/DELETE requests)
# สำหรับ GET requests อาจไม่ต้องใช้ CSRF token แต่ควรเตรียมไว้

print(f"✅ เริ่มต้นการวิเคราะห์ Group ID: {GROUP_IDS}")
print("-" * 30)

# --- 2. ฟังก์ชันหลักสำหรับเรียก API ---

def get_group_experiences(group_id):
    """ดึงรายการเกมทั้งหมดที่เป็นของกลุ่ม"""
    print(f"  -> ดึงเกมของกลุ่ม {group_id}...")
    url = f"https://games.roblox.com/v2/groups/{group_id}/games?sortOrder=Desc&limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # กรองเอา PlaceId และ UniverseId
        games = [{'name': item['name'], 'universeId': item['id'], 'placeId': item['placeId']} 
                 for item in data.get('data', [])]
        print(f"  -> พบ {len(games)} เกม")
        return games
    except requests.RequestException as e:
        print(f"  ❌ Error ดึงเกม: {e}")
        return []

def get_group_transactions(group_id, transaction_type="Sale"):
    """ดึงข้อมูลธุรกรรมของกลุ่ม (ต้องใช้สิทธิ์)"""
    # **ข้อควรระวัง:** การดึงข้อมูลธุรกรรมต้องการสิทธิ์และการยืนยันตัวตนผ่าน Cookie
    print(f"  -> ดึงธุรกรรม '{transaction_type}' ของกลุ่ม {group_id}...")
    url = f"https://economy.roblox.com/v1/groups/{group_id}/transactions?limit=10&transactionType={transaction_type}"
    try:
        response = requests.get(url, cookies=COOKIES)
        response.raise_for_status()
        data = response.json()
        
        # สร้าง DataFrame จากข้อมูลธุรกรรมล่าสุด
        df = pd.DataFrame(data.get('data', []))
        if not df.empty:
            df = df[['created', 'currency', 'amount', 'details']].head() # แสดงข้อมูลที่สำคัญ
            print(f"  -> ธุรกรรมล่าสุด (5 รายการ): \n{df.to_string(index=False)}")
        else:
            print("  -> ไม่พบข้อมูลธุรกรรม (หรือไม่มีสิทธิ์เข้าถึง)")
        
    except requests.RequestException as e:
        print(f"  ❌ Error ดึงธุรกรรม (อาจไม่มีสิทธิ์): {e}")

def get_game_revenue_stats(universe_id):
    """
    ดึงข้อมูล Revenue ของเกม (ต้องใช้สิทธิ์)
    *หมายเหตุ: API นี้ต้องการ UniverseId และสิทธิ์เฉพาะ
    """
    print(f"  -> ดึงสถิติรายได้ของ Universe ID {universe_id} (ตัวอย่าง)...")
    # **Endpoint ตัวอย่าง**: สำหรับการดึงสถิติรายได้อย่างละเอียดมักใช้ API ที่ซับซ้อนกว่า
    # และมักมีข้อจำกัดในการดึงข้อมูลย้อนหลัง
    url = f"https://develop.roblox.com/v1/places/{universe_id}/stats/Revenue?granularity=Daily&startTime=2025-11-01T00:00:00.000Z&endTime=2025-12-01T00:00:00.000Z"
    try:
        response = requests.get(url, cookies=COOKIES)
        response.raise_for_status()
        data = response.json()
        
        # แสดงผลลัพธ์บางส่วน
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            total_revenue = df['value'].sum()
            print(f"  -> Revenue รวม (Nov 2025): {total_revenue} Robux")
        else:
             print("  -> ไม่พบข้อมูล Revenue หรือไม่สามารถเข้าถึงสถิติได้")
    
    except requests.RequestException as e:
        print(f"  ❌ Error ดึง Revenue เกม (อาจไม่มีสิทธิ์): {e}")

# --- 3. การดำเนินการหลัก ---

def run_analysis():
    all_group_data = []
    
    for group_id in GROUP_IDS:
        print(f"\n======== วิเคราะห์กลุ่ม ID: {group_id} ========")
        group_data = {'groupId': group_id}

        # A. ดึงรายการเกมทั้งหมด
        games = get_group_experiences(group_id)
        group_data['games'] = games
        
        # B. วิเคราะห์รายได้ระดับกลุ่ม
        get_group_transactions(group_id, "Sale")
        
        # C. วิเคราะห์รายได้ระดับเกม
        if games:
            print("\n** เริ่มวิเคราะห์ Revenue ของแต่ละเกม (ตัวอย่าง 2 เกมแรก) **")
            for game in games[:2]: # ทดลองดึงแค่ 2 เกมแรก
                print(f"--- เกม: {game['name']} (Universe ID: {game['universeId']}) ---")
                get_game_revenue_stats(game['universeId'])

        all_group_data.append(group_data)

    print("\n✅ การวิเคราะห์เสร็จสมบูรณ์")

if __name__ == "__main__":
    run_analysis()
