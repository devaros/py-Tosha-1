import uasyncio as asyncio
from libs.kernel import Service
import random
import time
import json


from machine import Pin

class SchedTask():
  id = 0
  label = ''
  task = None
  schedule = "* * * * *"
  params = None
  enabled = False
  error = ''
  def __init__(self, enabled, schedule, id, params=None, label='', *args, **kwargs):
    self.id = id 
    self.schedule = schedule
    self.label = label
    self.params = params
    self.enabled = enabled
    #self.__dict__.update(kwargs)


class CronScheduler(Service):
    state = { 'time': None, "name": "cron_scheduler", "data": []}
    AW_LEN = 17
    task_list = []
    cmd_list = []

    def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.old_mm = None
      self.task_list = []
      self.reload()
          
    def reload(self):
      self.task_list = []
      try:
        with open('/crontab.json', 'r') as f:
          dd = json.loads(f.read())
          #self.state['data'] = dd
          for t in dd:
            self.task_list.append(SchedTask(*t))
        self.relink_task()
      except OSError as e:
        #print('Error open file', '/crontab.json')
        OSError ('Error open file /crontab.json')
        #raise e
      self.relink_task()

    def check_data(self):
      dd = self.state['data']
      if len(dd) in range(1,10):
        print('******')

    def check_tt(self, tt1, tt2 ):  # tt1- cron chank time,  tt2 - local time chank
      class T():
        str = 'str'
        range = 'range'
        list = 'list'

      #print("check_tt_0:", tt1, tt2)

      if tt1=='*':
        tt1 = None
        return True
      elif tt1.find('-')>0:
        tt1 = tt1.split('-')
        if len(tt1)>1:
          step = tt1[1].split('/')
          rng = range(int(tt1[0]), int(step[0])+1)
          if len(step)>1 and step[1].isdigit():
            return tt2 in rng and (tt2-int(tt1[0])) % int(step[1]) ==0
          else:
            return tt2 in tt1
      elif tt1.find(',')>0:
        tt1 = tt1.split(',')
        tt1 = [int(i) for i in tt1]
        return tt2 in tt1
      elif tt1.find('/')>=0:
        tt1 = tt1.split('/')
        if not tt1[0].isdigit(): tt1[0] = 0
        tt1 = (tt2-int(tt1[0])) % int(tt1[1])
        return tt1==0
      elif tt1==str(tt2):
        return True

    async def tic(self):
      yy, my, dd, hh, mm, _, dw, _,  = time.localtime()

      if self.old_mm == mm or yy<2022: return
      self.old_mm = mm

      for t in self.task_list:
        #i = i[1].split()
        #for i2 in t.schedule.split():
        i2 = t.schedule.split()
        try:
          if (t.enabled and t.task and self.check_tt(i2[0], mm) and
            self.check_tt(i2[1], hh) and self.check_tt(i2[2], dw+1) and
            self.check_tt(i2[3], dd)  and self.check_tt(i2[4], my)):
        
        #if i[0] == dd && i[1] == dw && i[2] == hh && i[3] == mm:
            #await i[4]()
            #asyncio.create_task( i[2](i[3]))
          #print("try_run_task:", hh, mm, t.id, t.task, type(t.params))
            print(f"run_task: {hh}:{mm}",  t.id, t.label, t.params)
            if type(t.params) in (list,tuple,int,): t.task(*t.params)  
            if type(t.params)==dict: t.task(**t.params)  
            #if i.task: i.task(i.params)  
            await asyncio.sleep(3)
        except Exception as e:
          print(f"run_task_error: {hh}:{mm}", t.id, t.label, t.params)
          t.error = "error"
          print (e)

      #self.state['time'] = time.time()

    #def link_task(self, id,  task, label, params=None):
    def append_command(self, id,  task, label, params=None):
      #dd = self.state['data']
      #tt = [i for i in self.task_list if i.id==id]
      #self.task_list.append((task,label,params))
      #if tt:
      self.cmd_list.append((task, id, label, params))
      self.relink_task()
      #for t in tt:
        #t.task = task
        #t.label = t.label or label
        #t.params = t.params if type(t.params) in (int,list,dict,) else params


    def relink_task(self):
      #dd = self.state['data']
      for task, id, label, params in self.cmd_list:
        tt = [i for i in self.task_list if i.id==id]
        #self.cmd_list.append((task, id, label, params))
        for t in tt:
          t.task = task
          t.label = t.label or label
          t.params = t.params if type(t.params) in (int,list,dict,) else params


    async def set_value(self, json_array):
      dd = json.dumps(json_array)  #, separators=(",\r\n", ":")
      dd = dd.replace("], [","],\r\n[")
      dd = dd.replace("[[","[\r\n[")
      dd = dd.replace("]]","]\r\n]")
      with open('/crontab.json', 'w') as f:
          f.write(dd)
      await asyncio.sleep(1)
      self.reload()


    def get_status(self):
        tasks = [(i.enabled, i.schedule, i.id,  i.params,  i.label,  ) for i in self.task_list ]
        #cmd_list = [(id, label, params, ) for _, id, label, params in self.cmd_list ]
        #return {"tasks":tasks, "cmd_list": cmd_list}
        return tasks

