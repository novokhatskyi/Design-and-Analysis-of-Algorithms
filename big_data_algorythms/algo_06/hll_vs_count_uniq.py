import re
import time
from datasketch import HyperLogLogPlusPlus
import pandas as pd

def load_ip_addresses(file_path):
    ip_read = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            match = ip_read.search(line.strip())
            if match:
                yield match.group(1)
            else:
                continue

def exact_count(file_path):
    """підрахунок через set"""
    unique_ips = set()
    for ip in load_ip_addresses(file_path):
        unique_ips.add(ip)
    return len(unique_ips)

def hll_count(file_path, p=16):
    """підрахунок через HyperLogLog++"""
    hll = HyperLogLogPlusPlus(p=p)
    for ip in load_ip_addresses(file_path):
        hll.update(ip.encode('utf-8'))
    return int(hll.count())

if __name__ == "__main__":
    file_path = 'big_data_algorythms/algo_06/log/lms-stage-access.log' 
    start_time = time.time()
    exact_result = exact_count(file_path)
    exact_time = time.time() - start_time
    # print(f"Exact count: {exact_result} (Time: {exact_time:.2f} seconds)")

    start_time = time.time()
    hll_result = hll_count(file_path, p=16)
    hll_time = time.time() - start_time
    # print(f"HyperLogLog++ estimate: {hll_result} (Time: {hll_time:.2f} seconds)")
    df = pd.DataFrame({
        'Method': ['Exact Count', 'HyperLogLog++'],
        'Unique IP': [exact_result, hll_result],
        'Time (seconds)': [exact_time, hll_time]
    })
    print(df)
