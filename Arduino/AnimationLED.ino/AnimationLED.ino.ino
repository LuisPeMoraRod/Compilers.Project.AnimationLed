// Column pin definitions
int columnDataPin = 2;
int columnLathPin = 3;
int columnClockPin = 4;

// Row pin definitions
int rowDataPin = 5;
int rowLathPin = 6;
int rowClockPin = 7;

// Time between animations
int timer = 1;

// Ground data for shift register 
byte gndData = 00000001;
byte gndDataFinal = 0;

// Each row of the animation
int row0, row1, row2, row3, row4, row5, row6, row7 = 0;

// Each row of the animation turned off
byte animationCleared[1][8] = {0, 0, 0, 0, 0, 0, 0, 0};

void setup() {

  // Inicialize serial port
  Serial.begin(9600);

  // Columns pins output definitions
  pinMode(columnDataPin, OUTPUT);
  pinMode(columnLathPin, OUTPUT);
  pinMode(columnClockPin, OUTPUT);

  // Row pins output definitions
  pinMode(rowDataPin, OUTPUT);
  pinMode(rowLathPin, OUTPUT);
  pinMode(rowClockPin, OUTPUT);   

}

void showAnimation (byte animation[1][8]) {

    for (byte i = 0; i < 1; i++) {

      for (byte j = 0; j < 8; j++) {
  
        byte columnData = animation[i][j];

        // Shift to the left the 1 bit
        byte gndDataFinal = gndData << j;

        // Denial of gndDataFinal 
        byte rowData =~ gndDataFinal;

        // Open lacth pins
        digitalWrite(rowLathPin, LOW);
        digitalWrite(columnLathPin, LOW);

        // Send row and column data
        shiftOut(rowDataPin, rowClockPin, MSBFIRST, rowData);
        shiftOut(columnDataPin, columnClockPin, MSBFIRST, columnData);      

        // Close lacth pins
        digitalWrite(rowLathPin, HIGH);
        digitalWrite(columnLathPin, HIGH);
                          
        delay(timer);    
  
      }
      
   }
  
}

void listenning() {

  // New message received
  if (Serial.available() > 0) {    
    
    String message = Serial.readStringUntil('\n');

    // Slicing the message received
    String messageFinal = "," + message.substring(1, message.length() - 1);
    
    int delimiter0, delimiter1, delimiter2, delimiter3, delimiter4, delimiter5,
        delimiter6, delimiter7, delimiter8;

    // Delimiters to know where are the important decimal numbers
    delimiter0 = messageFinal.indexOf(",");
    delimiter1 = messageFinal.indexOf(",", delimiter0 + 1);
    delimiter2 = messageFinal.indexOf(",", delimiter1 + 1);
    delimiter3 = messageFinal.indexOf(",", delimiter2 + 1);
    delimiter4 = messageFinal.indexOf(",", delimiter3 + 1);
    delimiter5 = messageFinal.indexOf(",", delimiter4 + 1);
    delimiter6 = messageFinal.indexOf(",", delimiter5 + 1);
    delimiter7 = messageFinal.indexOf(",", delimiter6 + 1);
    delimiter8 = messageFinal.indexOf(",", delimiter7 + 1);

    // Each row represent each decimal number received
    row0 = messageFinal.substring(delimiter0 + 1, delimiter1).toInt();
    row1 = messageFinal.substring(delimiter1 + 1, delimiter2).toInt();
    row2 = messageFinal.substring(delimiter2 + 1, delimiter3).toInt();
    row3 = messageFinal.substring(delimiter3 + 1, delimiter4).toInt();
    row4 = messageFinal.substring(delimiter4 + 1, delimiter5).toInt();
    row5 = messageFinal.substring(delimiter5 + 1, delimiter6).toInt();
    row6 = messageFinal.substring(delimiter6 + 1, delimiter7).toInt();
    row7 = messageFinal.substring(delimiter7 + 1, delimiter8).toInt();

    Serial.write("Animation changed");
         
  }

}

void loop() {  

  // Checking for new incoming message
  listenning();
  
  // Byte definition for current animation
  byte animation[1][8] = {row0, row1, row2, row3, row4, row5, row6, row7};

  // Show current animation
  showAnimation(animation);

  // Clear matriz from last aninimation
  showAnimation(animationCleared);  

}
