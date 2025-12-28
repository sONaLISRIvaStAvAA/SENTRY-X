#include <LiquidCrystal.h>

/* ---------- FUNCTION PROTOTYPES ---------- */
void safeState();
void presenceState();
void alertState();
void playAlert();

/* ---------- LCD ---------- */
LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

/* ---------- Ultrasonic ---------- */
const int trigPin = 9;
const int echoPin = 10;

/* ---------- RGB ---------- */
const int redPin = 8;
const int greenPin = 11;
const int bluePin = 13;

/* ---------- Buzzer ---------- */
const int buzzerPin = 12;

/* ---------- Variables ---------- */
long duration;
int distance;
unsigned long detectStart = 0;
bool intrusion = false;
bool songPlayed = false;

void setup() {
  delay(500);
  lcd.begin(16, 2);
  lcd.print("System Ready");

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  Serial.begin(9600);
}

void loop() {

  /* ----- RECEIVE VERIFIED FROM PYTHON ----- */
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'V') {              // VERIFIED
      intrusion = false;
      detectStart = 0;
      songPlayed = false;
    }
  }

  /* ----- ULTRASONIC ----- */
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, 30000);
  distance = duration * 0.034 / 2;

  if (distance > 0 && distance < 60) {
    if (detectStart == 0) detectStart = millis();
    if (distance < 30 && millis() - detectStart > 2000)
      intrusion = true;
  } else {
    intrusion = false;
    detectStart = 0;
  }

  /* ----- STATES ----- */
  if (intrusion) {
    presenceState();
    delay(300);
    alertState();
  }
  else if (distance > 0 && distance < 60) {
    presenceState();
  }
  else {
    safeState();
  }

  delay(400);
}

/* ---------- STATES ---------- */

void safeState() {
  Serial.println("SAFE");

  digitalWrite(redPin, LOW);
  digitalWrite(greenPin, HIGH);
  digitalWrite(bluePin, LOW);

  noTone(buzzerPin);
  songPlayed = false;

  lcd.clear();
  lcd.print("Monitoring");
  lcd.setCursor(0,1);
  lcd.print("SAFE!");
}

void presenceState() {
  Serial.println("PRESENCE");

  digitalWrite(redPin, HIGH);
  digitalWrite(greenPin, HIGH);
  digitalWrite(bluePin, LOW);

  noTone(buzzerPin);

  lcd.clear();
  lcd.print("Presence");
  lcd.setCursor(0,1);
  lcd.print("Detected!");
}

void alertState() {
  Serial.println("ALERT");

  digitalWrite(redPin, HIGH);
  digitalWrite(greenPin, LOW);
  digitalWrite(bluePin, LOW);

  if (!songPlayed) {
    playAlert();
    songPlayed = true;
  }

  lcd.clear();
  lcd.print("ALERT!");
  lcd.setCursor(0,1);
  lcd.print("INTRUSION");
}

void playAlert() {
  tone(buzzerPin, 1000, 200); delay(250);
  tone(buzzerPin, 1200, 200); delay(250);
  tone(buzzerPin, 1500, 400); delay(450);
  noTone(buzzerPin);
}
