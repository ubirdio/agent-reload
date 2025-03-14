for i in range(10):
    # Wait for input so we can fork the vm
    input(f"Press Enter to continue {i}...")

    # Do something that we'll replace between VM.
    if i % 2 == 0:
        print("Even")
    else:
        print("Odd")
