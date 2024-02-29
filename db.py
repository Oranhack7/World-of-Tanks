import subprocess
import time

def start_mongodb():
    # Start MongoDB server
    subprocess.Popen(["mongod"])

    # Wait for MongoDB to start
    time.sleep(3)  # Adjust delay as needed

if __name__ == "__main__":
    start_mongodb()
