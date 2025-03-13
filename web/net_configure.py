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
            data = await read_json(request)
            print("Request data:",   data)
            await self.net_manager.connect_to_network(data['ssid'], data['pswd'])
            return ' '
        elif request.method == "DELETE":
            self.net_manager.forget()
            #return json.dumps(aa_.state)
            return ' '


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
       
