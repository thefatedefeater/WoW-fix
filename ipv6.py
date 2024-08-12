V=32

import urllib.parse
from urllib.parse import quote
import os



from concurrent.futures import ThreadPoolExecutor, as_completed




import random

from icmplib import ping as pinging


def main_v6():
    global which
    global ping_range
    
    resultss=[]
    save_best=[]
    def generate_ipv6():
        return f"2606:4700:d{random.randint(0, 1)}::{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}"

    def ping_ip(ip, port, resultss, save_best):
        global do_you_save
        
        icmp=pinging(ip, count=4, interval=1, timeout=5,privileged=False)
        ping_ms=float(icmp.avg_rtt)
        jitter_ms=float(icmp.jitter)
        loss_rate_per=icmp.packet_loss
        if ping_ms == 0.0:
            ping_ms=1000
        
        if jitter_ms ==0.0:
            jitter_ms=1000
        
        if loss_rate_per ==1.0 :
            loss_rate_per=1000
        loss_rate_per=loss_rate_per*100
        if do_you_save=='1' and which !='3':
            
                
            
                if ping_ms<300 and loss_rate_per==0.0:
                    if which =='2':
                        if ping==int(ping_range):
                            save_best.append('['+ip+']'+'\n')
                    else:
                        if ping==int(ping_range):
                            save_best.append('['+ip+']'+',')
                
            
            
        
        combined_score = 0.5 * ping_ms + 0.3 * loss_rate_per + 0.2 * jitter_ms
        resultss.append((ip, port, ping_ms, loss_rate_per, jitter_ms,combined_score ))
        

    ports_to_check = [1074 , 864]

    random_ip=generate_ipv6()
    best_ping=1000
    best_ip=""



    
    
    resultss = []
    executor= ThreadPoolExecutor(max_workers=1000)
    try:
        for _ in range(101):
            executor.submit(ping_ip, generate_ipv6(), ports_to_check[random.randint(0,1)],resultss, save_best)
    except Exception as E:
            print('[bold red]An Error: [/bold red]', E)
    finally:
            executor.shutdown(wait=True)
            

    # Sort the results based on ping time
    sorted_results=sorted(resultss, key=lambda x: x[5])
    

    for ip, port,ping,loss_rate,jitter, combined_score  in sorted_results:

        if ping < best_ping:
            best_ping = ping
            best_ip = ip
        

    port_random = ports_to_check[random.randint(0, len(ports_to_check) - 1)]

    best_ip_mix = [1] * 2
    if best_ip:

        

        
        best_ip_mix[0] = "[" + best_ip + "]"

        best_ip_mix[1] = port_random
        
    else:


        
        best_ip_mix[0] = "[" + random_ip + "]"

                 
        
        best_ip_mix[1] = port_random
    with open('result.csv' , "w") as f:
        f.write(best_ip_mix)
