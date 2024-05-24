import requests
import urllib.parse
import json
import time
import subprocess
# URL dan headers
url = "https://api.service.gameeapp.com/"
headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Client-Language": "en",
    "Content-Type": "application/json",
    "Origin": "https://game.cyberfinance.xyz",
    "Referer": "https://game.cyberfinance.xyz/",
}

# Fungsi untuk membaca initData dari file
def read_initdata_from_file(filename):
    initdata_list = []
    with open(filename, 'r') as file:
        for line in file:
            initdata_list.append(line.strip())
    return initdata_list

# Fungsi untuk mengambil id dari initData
def get_user_id_from_init_data(init_data):
    parsed_data = urllib.parse.parse_qs(init_data)
    if 'user' in parsed_data:
        user_data = parsed_data['user'][0]
        user_data_json = urllib.parse.unquote(user_data)
        user_data_dict = json.loads(user_data_json)
        if 'id' in user_data_dict:
            return user_data_dict['id']
    return None

def get_nama_from_init_data(init_data):
    parsed_data = urllib.parse.parse_qs(init_data)
    if 'user' in parsed_data:
        user_data = parsed_data['user'][0]
        data = ""
        user_data_json = urllib.parse.unquote(user_data)
        user_data_dict = json.loads(user_data_json)
        if 'first_name' in user_data_dict:
            data = user_data_dict['first_name']
        if 'last_name' in user_data_dict:
            data = data + " " + user_data_dict['last_name']
        if 'username' in user_data_dict:
            data = data + " " + f"({user_data_dict['username']})"
        return data
    return None
# Fungsi untuk melakukan login menggunakan initData
def login_with_initdata(init_data):
    payload = {
            "initData": init_data
    }
    response = requests.post("https://api.cyberfinance.xyz/api/v1/game/initdata", json=payload, headers=headers)
    if response.status_code == 201:
        # Menambahkan header Authorization dari hasil response login
        auth_token = response.json()["message"]["accessToken"]
        headers["Authorization"] = f"Bearer {auth_token}"
    else:
        print(f"Failed to login. Error: {response.text}")
    return response

# Fungsi untuk melakukan start session
def start_session():
    response = requests.get('https://api.cyberfinance.xyz/api/v1/mining/claim', headers=headers)
    return response



# Fungsi untuk menjalankan operasi untuk setiap initData
def process_initdata(init_data):
    # Login
    nama = get_nama_from_init_data(init_data)
    login_response = login_with_initdata(init_data)
    if login_response.status_code == 201:
        print(f"Logged in successfully for user id: {nama}")            
         # Start session
        start_response = start_session()
        if start_response.status_code == 200:
            start_data = start_response.json()
            print(f"{start_data['userData']}")
        else :
            print('Belum Waktunya Claim')

                

    else:
        print(f"Failed to login. Error: {login_response.text}")

# Main program
def main():
    initdata_file = "initdata.txt"
    
    while True:
        initdata_list = read_initdata_from_file(initdata_file)
        
        for init_data in initdata_list:
            process_initdata(init_data.strip())
            print("\n")
        
        # Delay sebelum membaca ulang file initData
        time.sleep(0)  # Delay 60 detik sebelum membaca kembali file initData

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        subprocess.run(["python3.10", "gamee.py"])
