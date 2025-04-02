import uasyncio as asyncio
from libs.kernel import Service
import random
import time


from machine import Pin
led = None
pin0 = None
pin1 = None
pin2 = None
pin9 = None  # flash | boot


class SwitchesBoard_demo_c3(Service):
    #state = { 'time': None, "name": "switches", "label":"Switches demo" ,"type":"web_standard", "data": []}
    AW_LEN = 1

    def __init__(self, **kwargs):
      super().__init__(**kwargs)
      global led, pin0, pin1, pin2, pin9
      led = Pin(8, Pin.OUT, 1)
      pin0 = Pin(0, Pin.IN, Pin.PULL_UP)
      pin1 = Pin(1, Pin.OUT, 0)
      pin2 = Pin(2, Pin.IN, Pin.PULL_UP)
      pin9 = Pin(9, Pin.IN, Pin.PULL_UP)  # flash | boot


      self.state = { 'time': None, "name":kwargs.get('name') or self.name, "label":kwargs.get('label') or "Switches demo" ,"type":"web_standard", "data": []}
      if kwargs.get('group'):
        self.state['group'] = kwargs.get('group')

      #print ("self.state: ", self.state, self.AW_LEN)
      for id in range(9):
        self.state['data'].append(  {"id":id,"value": random.randrange(10,99999) } ) 

      self.state['data'][0]['name'] = 'room 1'
      self.state['data'][1]['name'] = 'room 2'
      self.state['data'][2]['name'] = 'room 3'
      self.state['data'][3]['name'] = 'room 4'
      self.state['data'][4]['name'] = 'room 5'

      self.state['data'][5]['name'] = 'Alarm'
      self.state['data'][6]['name'] = 'PIN-GPIO2'
      self.state['data'][7]['name'] = 'schedule-id-7'
      self.state['data'][8]['name'] = 'schedule-id-8'

      for i in self.state['data']:
        i["indicator"] = "digital" if i["id"]>4 else "analog"
        i["control"] = "digital" 



      self.alarm = [0,0]
      pin0.irq(trigger= Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.change_pin(0))
      #pin2.irq(trigger= Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.change_pin(pin2))
      pin9.irq(trigger= Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.change_pin(1))


    def change_pin(self, ind):
      ind_ = ind
      def change(val):
        self.alarm[ind_] = 1
        #print ("change_pin: ", pin_, pin_.value(), self.state['data'][id])
      return change

    def set_value(self, id, value):
      #if time.ticks_ms() / 1000 < 15: return
      for i in self.state['data']:
        if i['id'] == id:
          i['value'] = 1 if value else 0
          break
      if id==8: led.value(not value)
      if id==5: self.alarm[0] = 0
      if id==4: self.alarm[1] = 0

      #await self.subscribe_handler()
      asyncio.create_task( self.subscribe_handler())

    async def tic(self):
      #self.state['data'] = []
      #for id in range(5):
      if time.time() == self.state['time']: return
      tt =  time.time()
      if  time.time() % 20 ==0 :
        id = random.randrange(0,4)
        self.state['data'][id]['value'] = random.randrange(10,99999)
        self.state['time'] = tt

      if self.state['data'][4]['value'] !=  self.alarm[1]:
        self.state['data'][4]['value'] =  self.alarm[1]
        self.state['time'] = tt

      if self.state['data'][5]['value'] !=  self.alarm[0]:
        self.state['data'][5]['value'] =  self.alarm[0]
        self.state['time'] = tt


      if self.state['data'][6]['value'] !=  pin2.value():
        self.state['data'][6]["value"] = pin2.value()
        self.state['time'] = tt
        

      #self.state['data'][7] =  {"id":7,"value": 0 }
      #self.state['data'][8] =  {"id":8,"value": 0 }

      return self.state['time'] == tt # if we changed something

    def state_full__old2(self):
        #print(f"Состояние датчика {self.name}: {self.state}", self.pin)
        return {'name':self.name, 'type':self.__class__.__name__, 'state': self.state, 'info': self.info}   # данные в json формате


