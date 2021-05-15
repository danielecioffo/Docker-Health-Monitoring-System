from datetime import datetime
import time

if __name__ == '__main__':
    print(datetime.now(), " - I was created", flush=True)
    time.sleep(30)
    while 1:
        print(datetime.now(), " - I am running", flush=True)
        time.sleep(30)
