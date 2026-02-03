from voice.input import listen

def main():
    print("Personal Cognitive OS booting...")
    text = listen(seconds=10)
    print("Heard:", text)

if __name__ == "__main__":
    main()
