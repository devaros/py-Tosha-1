# objects/sensor.py
import uasyncio as asyncio
from hlbase import Object
#import random
from machine import Pin

sensors = []

available_pins= set ([1,2,3,4,5,6,7,8])

config=[
  {
    "name":"Цифровой датчик-1",
    #"type":"DiscreteSensor",
    "pin":12,
    "state_text":['off','on'],
    "alarm_state":0,
    "pull_mode":2,
  },
  {
    "name":"Цифровой датчик-3",
    #"type":"DiscreteSensor",
    "pin":14,
    "state_text":['down','up'],
    "alarm_state":0,
    "pull_mode":2,  
  }
]


class DiscreteSensor(Object):
    state = -1
    aw_len = 3
    info = ''

    def __init__(self, cfg):
      self.name = cfg['name']
      #self.pin = cfg['pin']
      self.pin = Pin(cfg['pin'], Pin.IN, cfg.get('pull_mode', Pin.PULL_UP))
      self.alarm_state = cfg['alarm_state']
      self.pull_mode = cfg['pull_mode']
      self.state_text = cfg.get('state_text',[0,1])
      self.info = f'{self.pin}'


    async def run(self):
        #await super().run()
        # Логика работы сенсора
        while True:
            #self.state = random.randint(100,999)
            self.state = self.state_text[self.pin.value()]
            #print(f"Цикл датчика ", self.state, self.pin)
            await asyncio.sleep(self.aw_len)


    def state_full(self):
        #print(f"Состояние датчика {self.name}: {self.state}", self.pin)
        return {'name':self.name, 'type':self.__class__.__name__, 'state': self.state, 'info': self.info}   # данные в json формате


def init_sensors(os_kernel):
    for cfg in config:
      s = DiscreteSensor(cfg)
      sensors.append(s)
      os_kernel.add_task(s)
    return sensors
     

#init_sensors()

