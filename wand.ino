#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Wire.h>
// #include <MPU6050.h>
#include <MPU6050_light.h>


#define LED 8

// BLE Service and Characteristic UUIDs
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
MPU6050 mpu(Wire);
const int buttonPin = 20; 
BLEServer* pServer = nullptr;
BLECharacteristic* pCharacteristic = nullptr;
bool deviceConnected = false;
int counter = 0;
// Server callbacks to handle events
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

void setup() {
  Serial.begin(9600);
  Serial.println("Starting BLE work!");


  // Initialize the BLE device
  BLEDevice::init("ESP32-C3-BLE");

  // Create BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_WRITE
                    );

  // Add a descriptor to the characteristic
  pCharacteristic->addDescriptor(new BLE2902());

  // Set the initial value for the characteristic
  pCharacteristic->setValue("Hello World!");

  // Start the service
  pService->start();

  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("Waiting for a client connection...");

  Wire.begin(8, 9); // SDA, SCL based on the pinout diagram
  // mpu.initialize();

  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while (status != 0) { } // stop everything if could not connect to MPU6050
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");

  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  // Do nothing here, everything is handled by BLE callbacks

  // if (deviceConnected) {
  //   // Do something if the device is connected
  //   ledON();
  //   delay(1000);
  //   ledOFF();
  //   delay(1000);
  // }
  // delay(1000);

  int16_t ax, ay, az, gx, gy, gz;
  bool buttonState = digitalRead(buttonPin) == LOW; // Button pressed when LOW
  mpu.update();
  // if (mpu.testConnection()) {
    //mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    // String data = String(counter)+","+String(ax) + "," + String(ay) + "," + String(az) + "," + String(gx) + "," + String(gy) + "," + String(gz) + "," + String(buttonState);
    String data = String(counter)+","+String(mpu.getAngleX())+","+String(mpu.getAngleY())+","+String(mpu.getAngleZ())+ "," + String(buttonState);
    Serial.println(data);
    delay(100);
    // Optional: Print data to Serial Monitor for debugging
    pCharacteristic->setValue(data);

    pCharacteristic->notify();
  // }
  delay(10);
  counter++;
  if (counter >= 10000){
    counter = 0;
  }


}

void ledON() {
  Serial.println("LED ON");
  digitalWrite(LED, LOW);
}

void ledOFF() {
  Serial.println("LED OFF");
  digitalWrite(LED, HIGH);
}