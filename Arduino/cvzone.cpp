#include "cvzone.h"

SerialData::SerialData(int numOfValsRec, int digitsPerValRec)
{
  _numOfValsRec = numOfValsRec;
  _digitsPerValRec = digitsPerValRec;
}

void SerialData::begin(int baudRate)
{
  Serial.begin(baudRate);
}

void SerialData::Send(int sendVals[])
{
  _sendString = "";
  for (int i = 0; i < _numOfValsSend; i++)
  {
    _sendString += String(sendVals[i]);
  }
  Serial.println(_sendString);
}

void SerialData::Get(int* valsRec)
{
  if (Serial.available())
  {
    _receivedString = Serial.readStringUntil('\n');

    for (int i = 0; i < _numOfValsRec; i++)
    {
      int indexStart = i * _digitsPerValRec;
      String val = _receivedString.substring(indexStart, indexStart + _digitsPerValRec);
      valsRec[i] = val.toInt();
    }
  }
}
