#include <Keypad.h>

const byte ROWS = 4; // Four rows
const byte COLS = 4; // Four columns

// Define the keypad layout (adjust if your keypad has different labels)
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; // Connect to the row pinouts of the keypad
byte colPins[COLS] = {5, 4, 3, 2}; // Connect to the column pinouts of the keypad

Keypad customKeypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  Serial.println("Arduino Ready! Press a key on the keypad.");
}

void loop() {
  char customKey = customKeypad.getKey();

  if (customKey) {
    // Only send the key if it's one of the numbers 1-9
    if (customKey >= '1' && customKey <= '9') {
      Serial.println(customKey); // Send the pressed key over serial
    }
  }
}