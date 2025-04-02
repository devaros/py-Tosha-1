#nano_api_server
import uasyncio as asyncio
import uerrno
import json


__version__ = '1.0.0'

http_status = {200:"200 OK", 401: '401 Unauthorized', 404: "404 Not Found",
  500: "500 Internal error", 501: "501 Not Implemented", 505: "505 Version Not Supported",}

cou_req=[0]  # if cou 8 it ceil

class HttpError(Exception):
    pass

class Response:
    status = "HTTP/1.1 200 OK\r\n"
    header = [
        "access-control-allow-origin: *\r\n",
        "access-control-allow-methods: {methods}\r\n",
    ]
    type = "text/javascript"

    def __init__(*args, **kwargs):
      pass

class Request:
    url = ""
    method = ""
    headers = {}
    route = ""
    read = None
    write = None
    close = None

    def __init__(self):
        self.url = ""
        self.method = ""
        self.headers = {}
        self.route = ""
        self.read = None
        self.write = None
        self.close = None

class EventData():  # handler
    def __init__(self, data):
      self.data = data


async def write(request, data):
    await request.write(
        data.encode('ISO-8859-1') if type(data) == str else data
    )


async def error(request, code, reason):
    await request.write("HTTP/1.1 %s %s\r\n" % (code, reason))
    #await request.write("access-control-allow-origin: *\r\n\r\n")  #123456
    await request.write("\r\n\r\n")  #123456
    print('request_error: ', code, request.url)
    await request.write("<h1>%s</h1>" % (reason))


async def send_file(request, filename, segment=64, binary=False):
    try:
        print('NW: ',filename)
        with open(filename, 'rb' if binary else 'r') as f:
            while True:
                data = f.read(segment)
                if not data:
                    break
                await request.write(data)
    except OSError as e:
        if e.args[0] != uerrno.ENOENT:
            raise
        raise HttpError(request, 404, f"File '{filename}' Not Found")


class Nanoweb:

    extract_headers = ('Authorization', 'Content-Length', 'Content-Type')
    headers = {}

    routes = []
    assets_extensions = ('html', 'css', 'js')

    callback_request = None
    callback_error = staticmethod(error)

    STATIC_DIR = '/web/ui'
    INDEX_FILE = STATIC_DIR + 'index.html'

    def __init__(self, port=80, address='0.0.0.0'):
        self.port = port
        self.address = address

    def route(self, route, index=0):
        """Route decorator"""
        def decorator(func):
            #self.routes[route] = func
            self.routes.insert(0,(route,func,))
            return func
        return decorator

    async def send_resp(self, request, data, status=200):
                await request.write( f"HTTP/1.1 {http_status[status]}\r\n")
                #await request.write( f"HTTP/2 {http_status[status]}\r\n")
                await request.write( "access-control-allow-origin: *\r\n")
                #await request.write("\r\n")

                #await request.write("Connection: close\r\n")
                #await request.write("Connection: keep-alive\r\n")
                #await request.write("Keep-Alive: timeout=1\r\n")

                #await asyncio.sleep(1)

                if isinstance(data, str):
                  #print('request_handler_44: ',  data)
                  #await request.write(f"Content-Length: {len(data)}\r\n")
                  #await request.write(f"Content-Length: 1\r\n")
                  await request.write( "Content-Type: text/html\r\n\r\n")
                  #await request.write( "Content-Type: application/json\r\n\r\n")
                  #await request.write( "\r\n\r\n")
                  await request.write(data)
                elif isinstance(data, dict):
                  dd_ = json.dumps(data)
                  #await request.write(f"Content-Length: {len(dd_)}\r\n")
                  await request.write( "Content-Type: application/json\r\n\r\n")
                  await request.write( dd_)

                #await request.write( "\r\n")
                await asyncio.sleep(1)
                #await request.close()

    async def generate_output(self, request, handler):
        """Generate output from handler

        `handler` can be :
         * dict representing the json
         * string, text content
         * tuple where the first item is dict or str and the second
           is the status
         * callable, the output of which is sent to the client
        """
        while True:
            if isinstance(handler, str) or isinstance(handler, dict):
                await self.send_resp(request, handler)

            elif isinstance(handler, tuple):
                #status = len(handler)>1 and http_status.get(handler[1]) or http_status[200]
                status = len(handler)>1 and handler[1] or 200
                #print('request_handler_33: ', handler, status)
                await self.send_resp(request, handler[0], status)

            else:
                handler = await handler(request)
                #print("handler .... else... ")
                if handler:
                    # handler can returns data that can be fed back
                    # to the input of the function
                    continue
            break

    async def handle(self, reader, writer):
        cou_req[0] +=1
        if cou_req[0]>5:
          print ('warn max-8-req: cou_req:', cou_req[0])

        items = await reader.readline()
        items = items.decode('ascii').split()
        if len(items) != 3:
            return

        request = Request()
        request.read = reader.read
        request.write = writer.awrite
        request.close = writer.aclose

        request.method, request.url, version = items

        try:
            try:
                if version not in ("HTTP/1.0", "HTTP/1.1"):
                    raise HttpError(request, 505, "Version Not Supported")

                while True:
                    items = await reader.readline()
                    items = items.decode('ascii').split(":", 1)

                    if len(items) == 2:
                        header, value = items
                        value = value.strip()

                        if header in self.extract_headers:
                            request.headers[header] = value
                    elif len(items) == 1:
                        break

                if self.callback_request:
                    self.callback_request(request)

                #if request.url in self.routes:
                if False:
                    # 1. If current url exists in routes
                    request.route = request.url
                    await self.generate_output(request,
                                               self.routes[request.url])
                else:
                    # 2. Search url in routes with wildcard
                    #for route, handler in self.routes.items():
                    for route, handler in self.routes:
                        if route == request.url \
                            or (route[-1] == '*'  and  request.url.startswith(route[:-1]) 
                                and route.count('/')<=request.url.count('/')
                            ):
                            request.route = route
                            await self.generate_output(request, handler)
                            break
                    else:
                        # 3. Try to load index file
                        if request.url in ('', '/'):
                            await send_file(request, self.INDEX_FILE)
                        else:
                            # 4. Current url have an assets extension ?
                            for extension in self.assets_extensions:
                                if request.url.endswith('.' + extension):
                                    await send_file(
                                        request,
                                        '%s/%s' % (
                                            self.STATIC_DIR,
                                            request.url,
                                        ),
                                        binary=True,
                                    )
                                    break
                            else:
                                raise HttpError(request, 404, "File Not Found")
            except HttpError as e:
                request, code, message = e.args
                await self.callback_error(request, code, message)
        except OSError as e:
            # Skip ECONNRESET error (client abort request)
            if e.args[0] != uerrno.ECONNRESET:
                raise
        finally:
            await writer.aclose()
            cou_req[0]-=1
            #print ('cou_req2:', cou_req[0])

    async def run(self):
        return await asyncio.start_server(self.handle, self.address, self.port)
