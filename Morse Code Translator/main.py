def text_to_morse(text):
    # Morse code dictionary
    morse_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '0': '-----', ' ': ' ', ',': '--..--', '.': '.-.-.-', '?': '..--..',
        '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
        ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
        '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
    }
    
    # Convert text to uppercase since morse code is case-insensitive
    text = text.upper()
    morse_text = []
    
    # Convert each character to Morse code
    for char in text:
        if char in morse_code:
            morse_text.append(morse_code[char])
    
    # Join with spaces between letters and return
    return ' '.join(morse_text)

def main():
    print("Welcome to the Morse Code Translator!")
    print("Enter 'quit' to exit the program.\n")
    
    while True:
        # Get input from user
        text = input("Enter text to convert to Morse code: ")
        
        # Check if user wants to quit
        if text.lower() == 'quit':
            print("\nThank you for using the Morse Code Translator!")
            break
        
        # Convert and display the morse code
        morse = text_to_morse(text)
        print(f"\nMorse Code: {morse}\n")

if __name__ == "__main__":
    main()
