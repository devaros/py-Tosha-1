from libs.kernel import os_kernel
from .nanowebapi import HttpError, EventData
#import asyncio
#import os, json,gc,time
from .webserver import read_json
       #, authenticate, get_custom_data, get_memory, get_custom_data, get_memory, CREDENTIALS
import json


class WebCron():
    def __init__(self, name, web):
        #super().__init__(name)
        #if web is None:
            #raise ValueError('not correct web')

        web.web_services.append( self.__class__.__name__)
        self.web=web
        self.web.app.route('/api/cron/ls*')(self.api_cron_ls)
        self.web.app.route('/api/cron/set*')(self.api_cron_set_val)


    #@authenticate(CREDENTIALS)
    async def api_cron_set_val(self, request):
        #print("Request api_switch_set_val: ")

        if request.method == "OPTIONS":
            await self.web.api_send_response(request)
            return

        if request.method in ("PUT","POST",):
          pass
        else:
            print("Method not allowed", request.method)
            raise HttpError(request, 501, "Not Implemented")

        grp_name = request.url.split('/')
        if len(grp_name)>4:
          grp_name = grp_name[5]
        else: grp_name = None
        
        aa_ = next(x for x in os_kernel.tasks  if x.name == 'CronScheduler')

        data = await read_json(request)
        print("Request data: ",  data)
        #await 
        await aa_.set_value( data)
        #aa_ = next(x for x in os_kernel.tasks  if x.name == 'CronScheduler')
        #print(f"api_switch_ls: {aa_}")
        #return json.dumps(aa_.state)
        return ' '

    def evt_changes(self, request):
        pass

    #@authenticate(CREDENTIALS)
    async def api_cron_ls(self, request):
        #vnt_data = EventData()

        #await request.write("HTTP/1.1 200 OK\r\n")
        #await request.write("access-control-allow-origin: *\r\n") #,immutable
        #await request.write("Content-Type: text/event-stream\r\n")
        #await request.write("Content-Type: text/event-stream\r\n")
        #await request.write("Cache-Control: no-cache\r\n")
        #await request.write("Connection: keep-alive\r\n\r\n")
        #err = [False]

        aa_ = next(x for x in os_kernel.tasks  if x.name == 'CronScheduler')
        if aa_:
          tasks = [(i.enabled, i.schedule, i.id,  i.params,  i.label,  ) for i in aa_.task_list ]
          cmd_list = [(id, label, params, ) for _, id, label, params in aa_.cmd_list ]
          return json.dumps({"tasks":tasks, "cmd_list": cmd_list})
          #return json.dumps( aa_.status)
    


