import asyncio
import os
import sys

def trace_calls(frame, event, arg):
    if event == 'call':
        code = frame.f_code
        print(f"Call to {code.co_name} in {code.co_filename}")
    return trace_calls

# sys.settrace(trace_calls)

async def main():
    print("Pre-import", flush=True)
    from app.container import container
    print("Post-import", flush=True)
    if container.memory:
        print("Memory search", flush=True)
        res = await container.memory.search("roadmap")
        print(f"Res len: {len(res)}", flush=True)
    else:
        print("No memory", flush=True)

if __name__ == "__main__":
    print("Main start", flush=True)
    asyncio.run(main())
