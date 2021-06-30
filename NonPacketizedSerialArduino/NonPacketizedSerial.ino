/*                  __  _____           _       __
   __  _____  ___  / /_/ ___/___  _____(_)___ _/ /
  / / / / _ \/ _ \/ __/\__ \/ _ \/ ___/ / __ `/ / 
 / /_/ /  __/  __/ /_ ___/ /  __/ /  / / /_/ / /  
 \__, /\___/\___/\__//____/\___/_/  /_/\__,_/_/   
/____/  

Non-Packatized Non-Blocking Serial of variable length to array.
Data in HEX format.

To be tested:
- Minimum Transfer Interval
- MCU Buffer
Probably not the best implemntation, but it works haha.                                          
 */


elapsedMillis ms;     //Specific to Teensy

const byte numBytes = 32;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;
uint8_t led = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("<Arduino is ready>");
  pinMode(13, OUTPUT);
}

void loop() {
  rxData();
  processRxData();

  if (ms > 500) {
    led = !led;
    ms = 0;
  }

  digitalWrite(13, led);

}

void rxData() {
  static byte ndx = 0;
  byte rb;


  while (Serial.available() > 0 && newData == false) {
    rb = Serial.read();
        receivedBytes[ndx] = rb;
        ndx++;

    if(!Serial.available()) {
      receivedBytes[ndx] = '\0'; // terminate the string
      numReceived = ndx;  // save the number for use when printing
      ndx = 0;
      newData = true;
    }
  }
}

void processRxData() {
  if (newData == true) {
    Serial.print("This just in (HEX values)... ");
    for (byte n = 0; n < numReceived; n++) {
      Serial.print(receivedBytes[n], HEX);
      Serial.print(' ');
    }
    Serial.println();
    newData = false;
  }
}
