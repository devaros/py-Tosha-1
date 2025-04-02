import uasyncio as asyncio
from libs.kernel import Service
import random
import time
from machine import Pin

class GPIO_board(Service):
    #state = {'time': None, "name": "GPIO_board", "label":"GPIO board control", "type":"web_standard", "data": []}
    AW_LEN = 1
    #pins = {}

    def __init__(self, pins:list, **kwargs):  ##pin(n, in/out, PULL)
      super().__init__(**kwargs)
      self.pins = {}
      self.state = { 'time': None, "name": kwargs.get('name') or self.name, "label": kwargs.get('label') or "GPIO board control", "type":"web_standard", "data": []}
      if kwargs.get('group'):
        self.state['group'] = kwargs.get('group')

      for p in pins:
        p_ = Pin(*p)
        #self.pins.append(p_)
        self.pins[p[0]] = p_
        el_ = {"id":p[0], "value":p_.value(), "name":"GPIO-"+str(p[0]) }   # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"
        #el_["values"] = {0:"off",1:"on"}
        el_["indicator"] = "digital"
        #el_["type"] = "analog"  # "analog-vertical"
        #el_["type"] = "select"
        #el_["measure"] = "%"  #text
        if Pin.OUT == (len(p)>1 and p[1]):
          el_["control"] = "digital"
          #el_["write"] = "analog"
          #el_["write"] = "select"
        self.state['data'].append(  el_ )  # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"

      el_ = {"id":42, "value":random.randrange(-10,40), "name":"Temp" }   # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"
      el_["indicator"] = "analog"
      el_["max"] = 40
      el_["min"] = -10
      el_["measure"] = "c"  #text
      self.state['data'].append(  el_ )  # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"

      el_ = {"id":43, "value":random.randrange(-10,40), "name":"Temp" }   # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"
      el_["indicator"] = "analog"
      el_["class"] = "bg-orange"
      el_["measure"] = "c"  #text
      self.state['data'].append(  el_ )  # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"


      el_ = {"id":44, "value":random.randrange(9,88), "name":"Tank" }   # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"
      el_["indicator"] = "analog"
      el_["alarm"] = 3  # 'top' | 'bottom' | 'left' | 'right'
      el_["direction"] = 'top'  # 'top' | 'bottom' | 'left' | 'right'
      el_["max"] = 99
      el_["min"] = 0
      el_["measure"] = "%"  #text
      self.state['data'].append(  el_ )  # "digital" # "analog:min:max:step" # "switch:[1,2,3,4,]"


    def set_value(self, id, value):
      #if time.ticks_ms() / 1000 < 15: return
      for i in self.state['data']:
        if i['id'] == id and i.get("control"):    #self.pins.get(id)
          self.pins[id].value(1 if value else 0)
          if i['value'] != self.pins[id].value():
            i['value'] = self.pins[id].value()
            self.state['time'] =  time.time()
            asyncio.create_task( self.subscribe_handler())
            break


    async def tic(self):
      tt =  time.time()

      for i in self.state['data']:
        #if i['id'] == id and i.get("control"):    #self.pins.get(id)
          #self.pins[id].value(1 if value else 0)
          if i["id"] in self.pins.keys() and i['value'] != self.pins[i["id"]].value():
            i['value'] = self.pins[i["id"]].value()
            self.state['time'] =  tt
          elif i["id"] == 42 and tt % 19 ==0:
            i['value'] = random.randrange(-25,40)
            self.state['time'] =  tt
          elif i["id"] == 43 and tt % 17 ==0:
            i['value'] = random.randrange(-25,40)
            self.state['time'] =  tt
          elif i["id"] == 44 and tt % 21 ==0:
            i['value'] = random.randrange(9,88)
            self.state['time'] =  tt

            #if self.state['time'] == tt:
            #print(f"tic__ : {self.state['time']}", i["id"])

      return self.state['time'] == tt # if we changed something  return True

    def state_full__old2(self):
        #print(f"Состояние датчика {self.name}: {self.state}", self.pin)
        return {'name':self.name, 'type':self.__class__.__name__, 'state': self.state, 'info': self.info}   # данные в json формате


