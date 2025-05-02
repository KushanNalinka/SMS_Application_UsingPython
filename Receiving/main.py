import threading
import config
from worker_thread import worker_loop
from logger import setup_logger

def main():
    setup_logger()  # Initialize logging

    threads = []
    for _ in range(config.NUM_THREADS):
        t = threading.Thread(target=worker_loop, daemon=True)
        t.start()
        threads.append(t)
    
    # Keep the main thread alive.
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
