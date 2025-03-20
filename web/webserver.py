# webserver.py
from .nanowebapi import Nanoweb,send_file,HttpError
import json
import os
from libs.kernel import Service, load
from ubinascii import a2b_base64 as base64_decode
import time
import gc
import asyncio

CREDENTIALS = ('foo', 'bar')

content_type = {'js':'text/javascript',  'svg':'image/svg+xml', 'json':'application/json', 'stream':'application/octet-stream'}

async def send_header_api(request, cnt_type='json'):
    await request.write("HTTP/1.1 200 OK\r\n")
    await request.write(f"Content-Type: {content_type[cnt_type]}\r\n")
    await request.write("access-control-allow-origin: *\r\n")
    await request.write("\r\n")


async def read_json(request):
    content_length = int(request.headers.get('Content-Length', 0))
    if content_length == 0:
        return None
    body = await request.read(content_length)
    return json.loads(body)


def get_uptime():
    uptime_s = int(time.ticks_ms() / 1000)
    #uptime_s = uptime_s % 60
    return uptime_s


def get_memory():
    return gc.mem_free()

def get_custom_data(requested_data):
    data = {}
    #for item in requested_data:
    #    print(item)
        #if item == 'date':
    data['datetime'] = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z'.format(*time.localtime())
        #elif item == 'currdir':
    data['currdir'] = os.getcwd()
        #elif item == 'time':
    #data['time'] = get_time()[1]
        #elif item == 'uptime':
    data['uptime'] = get_uptime()
        #elif item == 'mem_free':
    data['mem_free'] = get_memory()
        #elif item == 'sensor_list':
            #data['sensor_list'] = get_sensor_list()
    data['load'] = min(1,load[0])



        # Добавляйте сюда любые другие данные, которые могут потребоваться
    return data

def authenticate(credentials):
    async def fail(request):
        await request.write("HTTP/1.1 401 Unauthorized\r\n")
        await request.write('WWW-Authenticate: Basic realm="Restricted"\r\n\r\n')
        await request.write("<h1>Unauthorized</h1>")
        print("Authentication failed")

    def decorator(func):
        async def wrapper(self, request):
            header = request.headers.get('Authorization', None)
            if header is None:
                print("No Authorization header")
                return await fail(request)

            kind, authorization = header.strip().split(' ', 1)
            if kind != "Basic":
                print("Authorization type is not Basic")
                return await fail(request)

            authorization = base64_decode(authorization.strip()).decode('ascii').split(':')

            if list(credentials) != list(authorization):
                print("Credentials do not match")
                return await fail(request)

            return await func(self, request)

        return wrapper

    return decorator


class WebServer(Service):
    web_services = []

    def __init__(self, name, kernel):
        super().__init__(name)
        if kernel is None or not hasattr(kernel, 'tasks'):
            raise ValueError("not correct kernel")
        self.kernel = kernel
        self.app = Nanoweb(80)
        self.app.assets_extensions += ('ico',)
        self.app.STATIC_DIR = '/web/ui'
        print("WebServer initialized", )

        # Определение маршрутов
        self.app.route('/*')(self.ui)   # /web/ui
        self.app.route('/assets/*')(self.ui),
        self.app.route('/assets2/*')(self.ui),
        self.app.route('/ping')(self.ping)
        self.app.route('/sys_info')(self.sys_info)
        #self.app.route('/api/files')(self.api_files)
        #self.app.route('/api')(self.api_data)
        self.app.route('/api/data')(self.api_data)
        self.app.route('/api/status')(self.api_status)
        self.app.route('/api/api_long_rq')(self.api_long_rq)

    async def sleep(self, time):
        await asyncio.sleep(time)

    async def render_template(self, request, pages, context=None):
        print(f"Rendering template: {pages}")
        for page in pages:
            await send_file(request, f'/web/ui/{page}')


    #@authenticate(CREDENTIALS)
    async def api_data(self, request):
        data = await read_json(request)
        #print("Handling request for api_data", requested_data)
        #response_data = get_custom_data(requested_data)
        return get_custom_data(data)

        #await request.write("HTTP/1.1 200 OK\r\n")
        #await request.write("access-control-allow-origin: *\r\n") #,immutable
        #await request.write("Content-Type: application/json\r\n\r\n")
        #await request.write(json.dumps(response_data))
        #return json.dumps(response_data)

    #@authenticate(CREDENTIALS)
    async def ui(self, request):
        await request.write(b"HTTP/1.1 200 OK\r\n")

        args = {}
        #filename = request.url.split('/')[-1]
        fullname = request.url
        await request.write(f"Cache-Control: max-age=9915\r\n") #,immutable

        ext = request.url.split('/')[-1].split('.')
        ext = ext[-1] if len(ext)>1 else ''
        cnt_type = content_type.get(ext)
        if cnt_type: 
          await request.write(f"Content-Type: {cnt_type}\r\n")

        #if filename =='/' or ext: filename = '/index.html'
        if not ext: fullname = '/index.html'

        path = '/'.join( request.url.split('/')[:-1] )
#"/".join( "/asset/index.ggg".split('/')[:-1 ])
        files = os.listdir(self.app.STATIC_DIR+path)
        filenm = fullname.split('/')[-1]       
        if not filenm in files:
          if filenm+'.gz' in files:
            fullname+='.gz'
            args['binary']=True
            await request.write(f"Content-Encoding: gzip\r\n")

        #if ext=='svg': 
          #args = {'binary': True}

        #await request.write("Connection: keep-alive\r\n")
        #await request.write("Keep-Alive: timeout=5\r\n")
        os.listdir(self.app.STATIC_DIR)

        print("request.url: ", fullname, filenm, files )
        await request.write("\r\n")
        await send_file(
            request,
            '%s%s' % (self.app.STATIC_DIR, fullname),
            **args,
        )


    @authenticate(CREDENTIALS)
    async def sys_info(self, request):
        print("Handling request for sys_info")
        await request.write(b"HTTP/1.1 200 OK\r\n\r\n")
        await self.render_template(request, ('header.html','sys_info.html','footer.html'))

    #@authenticate(CREDENTIALS)
    async def api_status(self, request):
        #print("Handling request for api_status")
        await send_header_api(request)

        status = []
        #await request.write("[")
        for task in self.kernel.tasks:
            #status[task.name] = await task.get_status()
            status.append( task.status )
            #await asyncio.sleep(1)
            #await request.write( json.dumps( {task.name: await task.get_status()} ))
            #await request.write( ',\r\n')
        #response = '200 OK', json.dumps(status), {'Content-Type': 'application/json'}
        #await request.write("]")
        #response = json.dumps(status)
        await request.write(json.dumps(status))
        #await request.write("access-control-allow-origin: *\r\n") #,immutable
        #print(f"api_status response: {response} ")
        #aa_ = [(i.name, ) for i in self.__class__.get_instances() ]
        #print(f"api_status _insta: {aa_}")

        #return response

    #@authenticate(CREDENTIALS)
    async def ping(self, request):
        #print("Handling request for ping")
        #await request.write("HTTP/1.1 200 OK\r\n\r\n")
        #await request.write("pong")
        #print("Ping response sent")
        return 'pong'

    #@authenticate(CREDENTIALS)
    async def api_long_rq(self, request):
        await request.write("HTTP/1.1 200 OK\r\n")
        await request.write("access-control-allow-origin: *\r\n") #,immutable
        #await request.write("Content-Type: text/event-stream\r\n")
        await request.write("Content-Type: text/event-stream\r\n")
        await request.write("Cache-Control: no-cache\r\n")
        await request.write("Connection: keep-alive\r\n\r\n")
        for i in range(11):
          print("Handling request for: api_long_rq:",i)
          await request.write("event: " + "pp_rq_ok\r\n")
          await request.write("data: " + json.dumps({"id":time.time(), "data":{ "time":time.localtime(), 'test_data':i} } ))
          await request.write("\r\n")
          await request.write(f"id: {time.time()}\r\n")
          #await request.write( json.dumps({"id":time.time(), "event":"pp_rq_ok", "data":{ "time":time.localtime(), 'test_data':i} }))
          await request.write("\r\n")
          await asyncio.sleep(92)



    async def api_send_response(self, request, methods="DELETE, GET, POST, PUT, PATCH, OPTIONS", data=None):  # code=200, message="OK"
        #print(f"Sending response: 200 OK")
        await request.write(f"HTTP/1.1 200 OK\r\n")
        await request.write("access-control-allow-origin: *\r\n")
        await request.write(f"access-control-allow-methods: {methods}\r\n")
        await request.write("Content-Type: application/json\r\n\r\n")
        if data:
          await request.write(data)
        else:
          await request.write('{"status": true}')
        #print("Response sent")

    async def run(self):
        await asyncio.sleep(5)
        print("Starting web server")
 #       await asyncio.start_server(self.app.handle, self.app.address, self.app.port)
        await self.app.run()

    def get_status(self):
        #return json.dumps( {"routes":[i[0] for i in self.app.routes], 
        return {"routes":[i[0] for i in self.app.routes], 
          "port": self.app.port,
          #"name": self.name,
        }


