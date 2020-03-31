from serial import Serial
from time import sleep
from threading import Thread, Semaphore


class SerialSensors:

  def __init__(self):
  
    self.serial = Serial()
    self.lastReading = "No Data=0\n"
    self.getParams()
    self.portSem = Semaphore()
    self.varSem = Semaphore()
    self.recThread = Thread(target=self.recieve)
    self.txThread = Thread(target=self.transmit)
      
  def getParams(self):
  
    try:  
      f = open("serialParams.config", "r")
      lines = f.readlines()
      f.close()
      
      lines = [line.replace("\n", "") for line in lines]
      lines = [line.split("=") for line in lines]
      
      params = {}
      
      for line in lines:
        params.update({line[0].lower(): line[1]})
        
      self.serial.port = "COM1" if "port" not in params else params["port"]
      self.serial.baud = 9600 if "baud" not in params else int(params["baud"])
      self.serial.timeout = 3 if "timeout" not in params else int(params["timeout"])
    
    except:
      self.serial.port = "COM1"
      self.serial.baud = 9600
      self.serial.timeout = 3
      
  def recieve(self):
  
    while self.run:
      try:
      
        self.portSem.acquire()      
        result = self.serial.readline().decode("utf-8").replace("\n", "")
        self.portSem.release()
        
        if "=" in result:
          self.varSem.acquire()
          self.lastReading = result
          self.varSem.release()
              
        sleep(0.5)

      except:
        sleep(0.5)
        
  def transmit(self):
  
    while self.run:
    
      try:
        self.portSem.acquire()
        self.serial.write(b".")
        self.portSem.release()
      except:
        pass
      
      sleep(2)
      
    try:
        self.portSem.acquire()
        self.serial.write(b"*")
        self.portSem.release()
    except:
      pass
      
  def getData(self):
    self.varSem.acquire()
    result = self.lastReading
    self.varSem.release()
    return result
    
  def start(self):
    self.serial.open()
    self.run = True
    self.recThread.start()
    self.txThread.start()
    
  def stop(self):
    self.run = False
    self.txThread.join()
    self.recThread.join()
    self.serial.close()