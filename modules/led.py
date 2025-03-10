import uasyncio as asyncio

uid = "led_board_c3_1245345"

from machine import Pin
led = Pin(7, Pin.OUT)

json_template = {"uid": uid, "name": "led", "data": {"value":0,"type":"boolean","write":True}



class Board_Led_c3_1245345(Object):
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


