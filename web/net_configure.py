from libs.kernel import os_kernel
from .nanowebapi import HttpError
#import asyncio
#import os, json,gc,time
from .webserver import read_json
       #, authenticate, get_custom_data, get_memory, get_custom_data, get_memory, CREDENTIALS
import json


class NetConfig():
    def __init__(self, name, web, net_manager):
        #super().__init__(name)
        #if web is None:
            #raise ValueError('not correct web')

        web.web_services.append( self.__class__.__name__)
        self.web=web
        self.net_manager = net_manager
        self.web.app.route('/api/net/config*')(self.api_net_config)
        self.web.app.route('/api/net/scan')(self.api_net_scan)
        #self.web.app.route('/api/net_config*')(self.api_switch_set_val)


    #@authenticate(CREDENTIALS)
    async def api_net_config(self, request):
        print("Request api_switch_set_val: ")

        if request.method == "OPTIONS":
            await self.web.api_send_response(request, 'GET, PUT, POST, DELETE, OPTIONS')
            return

        if request.method in ["POST","PUT"]:
            #aa_ = next(x for x in os_kernel.tasks  if x.name == 'NetworkManager')
            data = await read_json(request)
            print("Request data:",   data)
            await self.net_manager.connect_to_network(data['ssid'], data['pswd'])
            return ' '
        elif request.method == "DELETE":
            self.net_manager.forget()
            #return json.dumps(aa_.state)
            return ' '



    #@authenticate(CREDENTIALS)
    async def api_net_config2__old2(self, request):
        await request.write("HTTP/1.1 200 OK\r\n")
        await request.write("access-control-allow-origin: *\r\n") #,immutable
        #await request.write("Content-Type: text/event-stream\r\n")
        await request.write("Content-Type: text/event-stream\r\n")
        await request.write("Cache-Control: no-cache\r\n")
        await request.write("Connection: keep-alive\r\n\r\n")
        err = [False]

        aa_ = next(x for x in os_kernel.tasks  if x.name == 'SwitchesBoard')
        async def scrib():
          try:
            await request.write("event: " + "message\r\n")
            await request.write("data: " + json.dumps(aa_.state) + "\r\n")
            await request.write(f"id: {aa_.state["time"]}\r\n")
            await request.write("\r\n")
          except Exception as e:
            err[0] = True

        aa_.subscribe( scrib )
        try:
          await scrib()
          for i in range(11):
            #aa_ = next(x for x in os_kernel.tasks  if x.name == 'SwitchesBoard')
            if err[0]:
              break
            print(f"api_switch_ls: {i} \n:: {aa_.state}")
            #await request.write("\r\n")  # check connected if error must return
            #await request.write("event: " + "msg\r\n")
            #await request.write("data: " + json.dumps(aa_) + "\r\n")
            #await request.write(f"id: {time.time()}\r\n")
            #await request.write("\r\n")
            await self.web.sleep(92)
        finally:
          print(f"api_switch_ls: close")
          aa_.unsubscribe(scrib)


    #@authenticate(CREDENTIALS)
    async def api_net_scan(self, request):
       import ubinascii

       res = [list(i) for i in self.net_manager.sta.scan()]
       for i in res:
         #if type(i[0]) ==bytes: 
           #i[0] = ubinascii.hexlify(i[0]).decode() 
         if type(i[1]) ==bytes: 
           i[1] = ubinascii.hexlify(i[1]).decode() 
       connected =  self.net_manager.sta.config('ssid')
       return json.dumps({"available":res, "connected":connected})
       
