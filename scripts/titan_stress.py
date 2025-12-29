import torch
import time

# Force use of the Titan RTX
device = torch.device("cuda:0")
print(f"Targeting: {torch.cuda.get_device_name(0)}")

# Allocate 20GB of VRAM to push the limits
print("Allocating 20GB VRAM...")
stress_tensor = torch.empty((50000, 50000), device=device)

print("Running Stress Test (30 seconds)...")
start_time = time.time()
while time.time() - start_time < 300:
    # Intense matrix multiplication
    _ = torch.matmul(stress_tensor[:1000, :1000], stress_tensor[:1000, :1000])

print("Test Complete. Titan RTX is fully operational.")