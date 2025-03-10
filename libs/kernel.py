# kernel.py
import uasyncio as asyncio
import _thread
import time

TREAD = True

class Kernel:
    def __init__(self):
        self.tasks = []
        print("Kernel initialized")

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task added: {task.name}")

    def start(self):
        print("Starting kernel")
        loop = asyncio.get_event_loop()
        for task in self.tasks:
            #print(f"Scheduling task: {task.name}")
            loop.create_task(task.run())

        if TREAD:
          print("Start Event Loop in thread: NonBlock Repl")
          #_ = _thread.stack_size(1111)  #STACK_SIZE
          _thread.start_new_thread(loop.run_forever, ())
        else:
          print("Start Event Loop: Block Repl")
          loop.run_forever()



class Service:
    _instances = []
    ALLOW_ARGS = ['state']
    AW_LEN = 1 # async await length min:1
    state = {}
    event_list = []

    def __init__(self, name=None):
        #self.name = name or self.__class__.__name__
        self.name =  self.__class__.__name__
        #self.AW_LEN = 1 # async await length
        Service._instances.append(self)

    def set_attr(self, **kwargs):
      # set any attr
      for arg in kwargs:
        if hasattr(self, arg) and (arg in self.ALLOW_ARGS):
          setattr(a , arg, kwargs[arg])

    def subscribe(self, proc):
      self.event_list.append(proc)

    def unsubscribe(self, proc):
      if proc in self.event_list:
        ind = self.event_list.index(proc)
        del self.event_list[ind]

    async def subscribe_handler(self):
        for proc in self.event_list:
          try:
            await proc()
          except Exception as e:
            self.unsubscribe(proc)

    # to do self proc
    async def tic(self):
      # to do self proc
      pass

    async def run(self):
        tt = 0
        while True:
            tt = time.time_ns() #/1000_000_000
            #tt = time.time()
            if await self.tic():
              await self.subscribe_handler()
            #tt = time.time_ns()/100000
            await asyncio.sleep(self.AW_LEN) #self.AW_LEN
            #load[0] =  min(1, (load[0] *8 + (time.time_ns()/1000_000 -tt)/1000  ) /9)
            load[0] =  min(0.9999, (load[0] *6 + ((time.time_ns() -tt)/1000_000_000 - self.AW_LEN )/(1)  ) /7)
            #load[0] =  min(1, (load[0] *6 + (time.time_ns()/1000_000_000 -tt +1)/(2)  ) /7)

    @property
    def status(self):
      return {"name":self.name, "state": self.get_status(), "AW_LEN":self.AW_LEN}

    def get_status(self):
        #return {"state": self.state, "name": self.name}
        return self.state

    @classmethod
    def get_instances(cls):
        return cls._instances


os_kernel = Kernel()
load = [0.2]