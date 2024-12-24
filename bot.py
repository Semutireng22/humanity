import os
import json
import time
from datetime import datetime, timedelta
import pytz
from web3 import Web3
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Banner
banner = r"""
██╗   ██╗ ██████╗ ██████╗      █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ 
██║   ██║██╔════╝ ██╔══██╗    ██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
██║   ██║██║  ███╗██║  ██║    ███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
██║   ██║██║   ██║██║  ██║    ██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝ 
╚██████╔╝╚██████╔╝██████╔╝    ██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║     
 ╚═════╝  ╚═════╝ ╚═════╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝                                                                               
====================================================
     BOT                : Hivera Minning 
     Telegram Channel   : https://t.me/UGDairdrop
====================================================
"""

print(Fore.CYAN + banner)

with open('config.json') as config_file:
    config = json.load(config_file)

private_keys = config.get("private_keys", [])

rpc_url = "https://rpc.testnet.humanity.org"
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    print(Fore.RED + "❌ Tidak dapat terhubung ke jaringan.")
    exit()

accounts = {web3.eth.account.from_key(key).address: key for key in private_keys}

def claim_reward(account, private_key):
    success = False
    while not success:
        try:
            transaction = {
                "chainId": 1942999413,
                "data": "0xb88a802f",
                "from": account,
                "gas": web3.to_hex(260000),
                "gasPrice": web3.to_hex(0),
                "nonce": web3.eth.get_transaction_count(account),
                "to": "0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7",
                "value": web3.to_hex(0),
            }
            print(Fore.LIGHTYELLOW_EX + f"└── 🔄 Mengirim transaksi untuk {account}...")

            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

            txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(Fore.GREEN + f"     └── ✅ Transaksi berhasil dikirim! Hash: {web3.to_hex(txn_hash)}\n")
            success = True
            
        except Exception as e:
            print(Fore.RED + f"⚠️ Gagal mengirim transaksi untuk {account}. Kesalahan: {str(e)}. Mencoba ulang dalam 10 detik...")
            time.sleep(10)

def time_until_next_claim():
    wib = pytz.timezone("Asia/Jakarta")
    now = datetime.now(wib)
    target_time = wib.localize(datetime.combine(now.date(), datetime.strptime("20:30", "%H:%M").time()))
    if now > target_time:
        target_time += timedelta(days=1)
    return (target_time - now).total_seconds()

# Fungsi utama
def start_claiming():
    try:
        # Klaim pertama segera
        print(Fore.YELLOW + "🚀 Sedang melakukan klaim")
        print(Fore.YELLOW + "=====================\n")
        for account, private_key in accounts.items():
            print(Fore.MAGENTA + f"🌟 Mengklaim reward untuk {account}...")
            claim_reward(account, private_key)
            time.sleep(5)

        while True:
            wait_time = time_until_next_claim()
            print(Fore.BLUE + f"⏳ Menunggu waktu klaim berikutnya... ({wait_time / 3600:.2f} jam)")
            time.sleep(wait_time)

            for account, private_key in accounts.items():
                print(Fore.MAGENTA + f"🌟 Mengklaim reward untuk {account}...")
                claim_reward(account, private_key)
                time.sleep(5)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n✅ Program selesai. Terima kasih telah menggunakan Humanity Daily!")

# Mulai klaim
start_claiming()
