from libs.kernel import os_kernel
from .nanowebapi import HttpError, EventData
#import asyncio
#import os, json,gc,time
from .webserver import read_json
       #, authenticate, get_custom_data, get_memory, get_custom_data, get_memory, CREDENTIALS
import json


class WebSwitches():
    def __init__(self, name, web):
        #super().__init__(name)
        #if web is None:
            #raise ValueError('not correct web')

        web.web_services.append( self.__class__.__name__)
        self.web=web
        self.web.app.route('/api/switches/ls*')(self.api_switch_ls)
        self.web.app.route('/api/switches/set*')(self.api_switch_set_val)


    #@authenticate(CREDENTIALS)
    async def api_switch_set_val(self, request):
        #print("Request api_switch_set_val: ")

        if request.method == "OPTIONS":
            await self.web.api_send_response(request)
            return

        if request.method != "PUT":
            print("Method not allowed", request.method)
            raise HttpError(request, 501, "Not Implemented")

        grp_name = request.url.split('/')
        if len(grp_name)>4:
          grp_name = grp_name[5]
        else: grp_name = None
        
        #aa_ = next(x for x in os_kernel.tasks  if x.name == 'Switches Board')
        aa_ = os_kernel.find_task('SwitchesBoard_demo_c3')

        data = await read_json(request)
        #print("Request data: ",  grp_name, data[0])
        #await 
        aa_.set_value( data[0]['id'], data[0]['value'])
        #print(f"api_switch_ls: {aa_}")
        #return json.dumps(aa_.state)
        return ' '

    def evt_changes(self, request):
        pass

    #@authenticate(CREDENTIALS)
    async def api_switch_ls(self, request):
        #vnt_data = EventData()

        await request.write("HTTP/1.1 200 OK\r\n")
        await request.write("access-control-allow-origin: *\r\n") #,immutable
        #await request.write("Content-Type: text/event-stream\r\n")
        await request.write("Content-Type: text/event-stream\r\n")
        await request.write("Cache-Control: no-cache\r\n")
        await request.write("Connection: keep-alive\r\n\r\n")
        err = [False]
        send_ = [False]
        #aa_ = next(x for x in os_kernel.tasks  if x.name == 'Switches Board')
        aa_ = os_kernel.find_task('SwitchesBoard_demo_c3')

        async def scrib():
          try:
            while send_[0]:
              await self.web.sleep(1)
            send_[0] = True

            await request.write("event: " + "message\r\n")
            await request.write("data: " + json.dumps(aa_.state) + "\r\n")
            await request.write(f"id: {aa_.state["time"]}\r\n")
            await request.write("\r\n")
          except Exception as e:
            err[0] = True
          finally:
            send_[0] = False

        aa_.subscribe( scrib )
        #print(f"api_switch_ls: start")

        try:
          await scrib()
          for i in range(11):
            if err[0]:
              break
            #print(f"api_switch_ls: {i} \n:: {aa_.state}")
            #await request.write("\r\n")  # check connected if error must return
            #await request.write("event: " + "msg\r\n")
            #await request.write("data: " + json.dumps(aa_) + "\r\n")
            #await request.write(f"id: {time.time()}\r\n")
            #await request.write("\r\n")
            await self.web.sleep(92)
        finally:
          #print(f"api_switch_ls: close")
          aa_.unsubscribe(scrib)
        #return vnt_data
