import GPUtil
from prettytable import PrettyTable

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    table = PrettyTable(['GPU ID', 'Total Memory (GB)', 'Used Memory (GB)', 'Free Memory (GB)'])
    
    for gpu in gpus:
        total_vram = gpu.memoryTotal / 1024
        used_vram = gpu.memoryUsed / 1024
        free_vram = gpu.memoryFree / 1024
        table.add_row([gpu.id, f"{total_vram:.2f}", f"{used_vram:.2f}", f"{free_vram:.2f}"])
    
    print(table)

get_gpu_info()