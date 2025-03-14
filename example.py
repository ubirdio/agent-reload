# /// script
# dependencies = [
# "requests"
# ]
# ///
import time
import ai_dev

@ai_dev.in_ai_dev()
def inner(recordings, i):
    recordings.append(f"{i} - {time.time()} - original")
    print(f"Here's the record: {recordings}")

def example():
    recordings = []
    for i in range(10):
        inner(recordings, i)

if __name__ == "__main__":
    example()
