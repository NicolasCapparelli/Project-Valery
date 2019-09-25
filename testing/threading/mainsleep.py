from threading import Event
import threading
import time

# Event
run_main = Event()


# Main thread
def main():

    # While the Event's flag is not set to true
    while not run_main.is_set():

        # Essentially makes the main thread sleep for 60 seconds or until the flag is set to to true
        run_main.wait(60)

    # What happens after the main thread is done sleeping
    print("DONE")


def second_thread():

    # Sleep for 5 seconds
    time.sleep(5)

    # Set the events flag to true, causing the main thread to wake up
    run_main.set()


if __name__ == "__main__":

    # Launching second thread
    some_thread = threading.Thread(target=second_thread())
    some_thread.start()

    # Launching main thread
    main()


