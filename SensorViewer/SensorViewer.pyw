from tkinter import Tk, Frame, Label, StringVar, Button
from serialSensors import SerialSensors
from sys import exit
from time import time


class BadDataPanel(Frame):

  def __init__(self, root):
    Frame.__init__(self, root)
    self.root = root
    
    self.lbl = Label(self, text="Unable to open serial port.")
    self.btn = Button(self, text="OK")
    
    self.btn.bind("<Button-1>", self.close)
    
    self.lbl.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nesw")
    self.btn.grid(row=1, column=1, padx=5, pady=5, sticky="nesw")
    
  def close(self, event):
    self.root.destroy()


class SensorTable(Frame):
  
  def __init__(self, root):
    Frame.__init__(self, root, bg="#BBBBBB", bd=1)    
    self.columnconfigure(0, weight=1)    
    
    # init lists
    self.nRows = 0
    self.labelrows = []
    self.currentrows = []
    self.minrows = []
    self.maxrows = []
    self.labels = []
    self.current = []
    self.minlbls = []
    self.labelvars = []
    self.maxlbls = []
    self.minvars = []
    self.maxvars = []
    
    # build header
    self.headerCols = [Frame(self, bg="#FFFFFF") for i in range(4)]
    self.headerlbls = []
    self.headerlbls.append(Label(self.headerCols[0], text="Sensor", bg="#FFFFFF"))
    self.headerlbls.append(Label(self.headerCols[1], text="Current", bg="#FFFFFF"))
    self.headerlbls.append(Label(self.headerCols[2], text="Min.", bg="#FFFFFF"))
    self.headerlbls.append(Label(self.headerCols[3], text="Max.", bg="#FFFFFF"))    
    self.headerlbls[0].grid(row=0, column=0, sticky="w", padx=5)
    self.headerlbls[1].grid(row=0, column=0, sticky="e", padx=5)
    self.headerlbls[2].grid(row=0, column=0, sticky="e", padx=5)
    self.headerlbls[3].grid(row=0, column=0, sticky="e", padx=5)
    self.headerCols[0].grid(row=0, column=0, sticky="nesw")
    self.headerCols[1].grid(row=0, column=1, sticky="nesw")
    self.headerCols[2].grid(row=0, column=2, sticky="nesw")
    self.headerCols[3].grid(row=0, column=3, sticky="nesw")
    

  def build(self, firstReading):
  
    # destroy all existing objects
    for i in range(self.nRows):
      self.labelrows[i].destroy()
      self.currentrows[i].destroy()
      self.minrows[i].destroy()
      self.maxrows[i].destroy()
      self.labels[i].destroy()
      self.current[i].destroy()
      self.minlbls[i].destroy()
      self.maxlbls[i].destroy()
      self.labelvars[i] = None
      self.currentvars[i] = None
      self.minvars[i] = None
      self.maxvars[i] = None

    # recreate lists
    self.labelrows = []
    self.currentrows = []
    self.minrows = []
    self.maxrows = []
    self.labels = []
    self.current = []
    self.minlbls = []
    self.maxlbls = []
    self.labelvars = []
    self.minvars = []
    self.maxvars = []
    self.currentvars = []
  
    data = firstReading.replace("\n", "").split(";")
    data = [d.split("=") for d in data]
    colors = ["#DDDDDD", "#FFFFFF"]
    
    self.nRows = len(data)
    
    for i in range(self.nRows):
      
      self.labelrows.append(Frame(self, bg=colors[i % 2]))
      self.labelrows[i].columnconfigure(0, weight=1)
      
      self.currentrows.append(Frame(self, bg=colors[i % 2]))
      self.currentrows[i].columnconfigure(0, weight=1)
      
      self.minrows.append(Frame(self, bg=colors[i % 2]))
      self.minrows[i].columnconfigure(0, weight=1)
      
      self.maxrows.append(Frame(self, bg=colors[i % 2]))
      self.maxrows[i].columnconfigure(0, weight=1)
    
      self.labelvars.append(StringVar())
      self.labelvars[i].set(data[i][0])
      self.currentvars.append(StringVar())
      self.currentvars[i].set(data[i][1])
      self.minvars.append(StringVar())
      self.minvars[i].set(data[i][1])
      self.maxvars.append(StringVar())
      self.maxvars[i].set(data[i][1])
      
      self.labels.append(Label(self.labelrows[i], bg=colors[i % 2], textvariable=self.labelvars[i]))
      self.current.append(Label(self.currentrows[i], bg=colors[i % 2], textvariable=self.currentvars[i]))
      self.minlbls.append(Label(self.minrows[i], bg=colors[i % 2], textvariable=self.minvars[i]))
      self.maxlbls.append(Label(self.maxrows[i], bg=colors[i % 2], textvariable=self.maxvars[i]))     
      
      self.labelrows[i].grid(row=i+1, column=0, sticky="ew")
      self.currentrows[i].grid(row=i+1, column=1, sticky="ew")
      self.minrows[i].grid(row=i+1, column=2, sticky="ew")
      self.maxrows[i].grid(row=i+1, column=3, sticky="ew")
      
      self.labels[i].grid(row=0, column=0, padx=5, sticky="w")
      self.current[i].grid(row=0, column=0, padx=5, sticky="e")
      self.minlbls[i].grid(row=0, column=0, padx=5, sticky="e")
      self.maxlbls[i].grid(row=0, column=0, padx=5, sticky="e")
    
  def setValues(self, data):
    try:
      vals = data.replace("\n", "").split(";")
      if len(vals) != self.nRows:
        self.build(data)
        return
      vals = [v.split("=") for v in vals]
      for i in range(self.nRows):
        if vals[i][0] != self.labelvars[i].get():
          self.build(data)
          return
        self.currentvars[i].set(vals[i][1])
        try:
          val = float(vals[i][1])
          if val > float(self.maxvars[i].get()):
            self.maxvars[i].set(vals[i][1])
          elif val < float(self.minvars[i].get()):
            self.minvars[i].set(vals[i][1])
        except:
          pass
    except:
      pass
      
      
class MainPanel(Frame):

  def __init__(self, root, sensor):
    Frame.__init__(self, root)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)
    
    self.root = root
    self.sensor = sensor
    self.starttime = time()
    self.timevar = StringVar()
    self.timevar.set("0:00:00")
    
    self.sensors = SensorTable(self)
    self.rst = Button(self, text="Reset")
    self.rst.bind("<Button-1>", self.reset)
    self.timelbl = Label(self, text="Run Time:")
    self.timeval = Label(self, textvariable=self.timevar)
    
    self.sensors.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="new")
    self.timelbl.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    self.timeval.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    self.rst.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    
    self.reset(None)
    
  def refresh(self):
    self.refreshRunTime()
    self.sensors.setValues(self.sensor.getData())
    self.root.after(50, self.refresh)
  
  def reset(self, event):
    data = self.sensor.getData()
    self.sensors.build(data)
    self.starttime = time()
    self.refreshRunTime()
    
  def refreshRunTime(self):
    dt = int(time() - self.starttime)
    hours = str(dt // 3600)
    dt = dt % 3600
    minutes = ("0" + str(dt // 60))[-2:]
    seconds = ("0" + str(dt % 60))[-2:]
    self.timevar.set(hours + ":" + minutes + ":" + seconds)
	
  def exit(self):
    self.sensor.stop()
    exit()
    

if __name__ == "__main__":  
  root = Tk()
  root.wm_title("SensorViewer")
  sensor = SerialSensors()
  
  try:
    sensor.start()
    mp = MainPanel(root, sensor)
    mp.pack(padx=5, pady=5)
    root.protocol("WM_DELETE_WINDOW", mp.exit)
    root.after(50, mp.refresh)
  except Exception as e:
    bd = BadDataPanel(root)
    bd.pack()
    print(str(e))
    
  root.mainloop()