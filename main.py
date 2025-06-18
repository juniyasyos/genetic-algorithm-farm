# === main.py ===

from threaded_main import run_ga  
import threading

def main():
    thread_configs = [
        ("thr-1", 5_000),
        ("thr-2", 10_000),
        ("thr-3", 15_000),
    ]

    threads = []
    for name, gens in thread_configs:
        t = threading.Thread(target=run_ga, args=(name, gens))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
