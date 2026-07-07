import os, time, json, requests
from send_zkr import send_zkr_sync

TREASURY_ADDRESS = "UQBbWHxNpPeI0oXO6OIfR3alZ9T9T40pR_BDRPvYyqSsl-Kl"
PROCESSED_FILE = "processed_liquidity_tx.json"
TOKENS_PER_5TON = 15000
MIN_TON_NANO = 4_900_000_000

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE) as f:
            return set(json.load(f))
    return set()

def save_processed(s):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(s), f)

def get_incoming_transactions():
    url = f"https://toncenter.com/api/v3/transactions?account={TREASURY_ADDRESS}&limit=20&sort=desc"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json().get("transactions", [])

def main_loop():
    processed = load_processed()
    print("Monitor started...")
    while True:
        try:
            for tx in get_incoming_transactions():
                tx_hash = tx.get("hash")
                if not tx_hash or tx_hash in processed:
                    continue
                in_msg = tx.get("in_msg") or {}
                value = int(in_msg.get("value") or 0)
                source = in_msg.get("source")
                if source and value >= MIN_TON_NANO:
                    print(f"New payment: {value} nanoTON from {source}")
                    try:
                        send_zkr_sync(source, TOKENS_PER_5TON)
                        print(f"Sent {TOKENS_PER_5TON} ZKR to {source}")
                    except Exception as e:
                        print(f"FAILED sending to {source}: {e}")
                        continue
                processed.add(tx_hash)
            save_processed(processed)
        except Exception as e:
            print(f"Monitor error: {e}")
        time.sleep(20)

if __name__ == "__main__":
    main_loop()
