import random
import time

NOF_PACKETS = 10 
def get_random_size(max_val):
    rn = (random.randint(0, 9)) % max_val
    return 1 if rn == 0 else rn

def main():
    p_sz_rm = 0 

  
    packet_sz = [get_random_size(6) * 10 for _ in range(NOF_PACKETS)]

    for i, size in enumerate(packet_sz):
        print(f"packet[{i}]: {size} bytes")

  
    o_rate = int(input("\nEnter the Output rate: "))
    b_size = int(input("Enter the Bucket Size: "))

    for i in range(NOF_PACKETS):
  
        if (packet_sz[i] + p_sz_rm) <= b_size:
            p_sz_rm += packet_sz[i]
            print("\n" + "-"*43)
            print(f"Incoming Packet size: {packet_sz[i]} bytes")
            print(f"Bytes remaining to Transmit: {p_sz_rm}")
            
      
            p_time = get_random_size(4) * 10
            print(f"Time left for transmission: {p_time} units")

    
            for clk in range(10, p_time + 1, 10):
                time.sleep(1)
                if p_sz_rm > 0:
                    if p_sz_rm <= o_rate:
                        op = p_sz_rm
                        p_sz_rm = 0
                    else:
                        op = o_rate
                        p_sz_rm -= o_rate
                    print(f"Packet of size {op} Transmitted")
                    print(f"Bytes Remaining to Transmit: {p_sz_rm}")
                else:
                    print(f"Time left for transmission: {p_time - clk} units")
                    print("No packets to transmit!!")
        else:
            print("\n" + "-"*43)
            print(f"Incoming packet size ({packet_sz[i]} bytes) + current buffer ({p_sz_rm} bytes) exceeds Bucket capacity ({b_size} bytes) - PACKET REJECTED!!")

if __name__ == "__main__":
    main()
                                                                                                                                                                                                                                                                                                                                                                                                       

