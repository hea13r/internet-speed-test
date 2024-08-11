import speedtest
import concurrent.futures
import threading
import time

def test_speed(test_type):
    st = speedtest.Speedtest()
    st.get_best_server()
    if test_type == 'download':
        return st.download() / 1_000_000  # Convert to Mbps
    elif test_type == 'upload':
        return st.upload() / 1_000_000  # Convert to Mbps

def show_progress(indicator, stop_event):
    while not stop_event.is_set():
        print(indicator, end="", flush=True)
        time.sleep(1)

def main():
    # Create event objects for stopping progress threads
    stop_event_download = threading.Event()
    stop_event_upload = threading.Event()

    # Perform download speed test
    print("Testing download speed...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        progress_thread_download = threading.Thread(target=show_progress, args=('v', stop_event_download))
        progress_thread_download.start()

        future_download = executor.submit(test_speed, 'download')
        download_speed = future_download.result()

        # Stop download progress thread
        stop_event_download.set()
        progress_thread_download.join()

    # Print download speed result
    print(f"\nDownload Speed: {download_speed:.2f} Mbps")

    # Perform upload speed test
    print("Testing upload speed...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        progress_thread_upload = threading.Thread(target=show_progress, args=('^', stop_event_upload))
        progress_thread_upload.start()

        future_upload = executor.submit(test_speed, 'upload')
        upload_speed = future_upload.result()

        # Stop upload progress thread
        stop_event_upload.set()
        progress_thread_upload.join()

    # Print upload speed result
    print(f"\nUpload Speed: {upload_speed:.2f} Mbps")

    st = speedtest.Speedtest()
    st.get_best_server()
    ping = st.results.ping
    print(f"Ping: {ping:.2f} ms")

if __name__ == "__main__":
    main()
