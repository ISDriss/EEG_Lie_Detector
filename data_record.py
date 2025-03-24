import os
import time
import muselsl as msl
from multiprocessing import Process
from muse_record import record

def stream(address):
    msl.stream(address)

def view(version):
    msl.view(version=version)

def default_menu(stream_process, view_process):
    while True:
        print("Menu:")
        print("1. Start recording")
        print("2. Stop streaming")
        choice = input("Enter your choice: \n")

        if choice == '1':
            # record file to the correct folder
            data_folder = os.path.join(os.getcwd(), "data")
            filename = os.path.join(data_folder, "%s_recording_%s.csv" %("EEG",time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime())))

            # Get recording duration from user input
            try:
                duration = int(input("Enter the recording duration in seconds: "))
            except ValueError:
                print("Invalid duration. Please enter a numeric value.")
                continue

            record_process = Process(target=record, args=(duration, filename))
            record_process.start()
            record_process.join()
        elif choice == '2':
            view_process.kill()
            stream_process.kill()
            break
        else:
            print("Invalid choice. Please try again.")

def setup():
    address = ""

    # List available Muses
    muses = msl.list_muses()
    if len(muses) < 1:
        print("No devices found")
        return

    # Get the address of the first Muse
    address = muses[0]["address"]
    print(f"Device address: {address}")

    # Start the stream process
    stream_process = Process(target=stream, args=(address,))
    stream_process.start()

    # Give the stream some time to start
    time.sleep(10)

    # Start the view process
    view_process = Process(target=view, args=(2,))
    view_process.start()

    default_menu(stream_process, view_process)

if __name__ == "__main__":
    setup()