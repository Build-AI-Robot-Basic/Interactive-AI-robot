#ifndef CVZONE_H
#define CVZONE_H

#include <Arduino.h>

class SerialData
{
  private:
    int _numOfValsSend;
    String _sendString;
    String _receivedString;
    int _numOfValsRec;
    int _digitsPerValRec;

  public:
    SerialData(int numOfValsRec = 1, int digitsPerValRec = 1);
    void begin(int baudRate = 9600);
    void Send(int sendVals[]);
    void Get(int* valsRec);
};

#endif