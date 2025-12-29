from router import route_query
import time

print("--- Testing L1 Layer (Titan RTX) ---")
start_time = time.time()
question = "Write a python function to calculate fibonacci numbers."
answer = route_query(question)
end_time = time.time()

print(f"\nResponse:\n{answer}")
print(f"\n--- Inference took {end_time - start_time:.2f} seconds ---")
