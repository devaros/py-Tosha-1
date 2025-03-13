from .nanowebapi import send_file,HttpError
from .webserver import send_header_api, authenticate, get_custom_data, get_memory, get_custom_data, get_memory, CREDENTIALS
from libs.kernel import Service
import os, json,gc,time

class Files(Service):
    def __init__(self, name, web):
        super().__init__(name)
        if web is None:
            raise ValueError('not correct web')

        web.web_services.append( self.__class__.__name__)
        self.web=web
        #self.web.app.route('/files')(self.files)
        self.web.app.route('/api/ls*')(self.api_ls)
        self.web.app.route('/api/download/*')(self.api_download)
        self.web.app.route('/api/delete/*')(self.api_delete) #TODO
        self.web.app.route('/api/upload/*')(self.upload)
        self.web.app.route('/show_content*')(self.show_content)

#TODO удаление, редактирование
    #@authenticate(CREDENTIALS)
    #async def files(self, request):
        #print("Handling request for files")
        #await request.write(b"HTTP/1.1 200 OK\r\n\r\n")
        #await self.web.render_template(request, ('header.html', 'files.html', 'footer_noscript.html'))


    #@authenticate(CREDENTIALS)
    async def api_ls(self, request):
        print("Handling request for api_ls")
        #await request.write("HTTP/1.1 200 OK\r\n")
        request_commands=str(request.url).split('?')
        if len(request_commands)>1:
            if request_commands[1].count('chdir=')>0:
                dir_name=request_commands[1].split('=')[1]
                #print("dir_name: ", dir_name)
                os.chdir(dir_name)
        currdir=os.getcwd()
        if currdir!='/':
            pref=['/','..']
        else:
            pref=[]
        await send_header_api(request)
        #await request.write("Content-Type: application/json\r\n")
        #await request.write("access-control-allow-origin: *\r\n") #,immutable
        #await request.write("\r\n")

        #file_list = ', '.join('"' + f + '"' for f in pref+sorted(os.listdir()))
        #await request.write(f'{{"files": [{file_list}]}}')
        #stat = os.stat(f) #0 -type, 6 - size lambda os.stat(f): (f[0], f[6])
        stat = lambda x: [x[0], x[6]]
        dd = [[f]+ stat(os.stat(f))  for f in  pref+sorted(os.listdir())]
        #dd = [[f]+ lambda os.stat(f): [f[0], f[6]] ) for f in  pref+sorted(os.listdir())]
        # print('file size:', Stat[6])
        import uos
        ffd = uos.statvfs('/')
        total = ffd[0]*ffd[2]
        free = ffd[1]*ffd[3]
        await request.write(json.dumps( {"files":dd, "currdir":currdir, "total":total, "free":free, "used":total-free,} ))
        #print(f"api_ls response: {file_list}")



    #@authenticate(CREDENTIALS)
    async def api_delete(self, request):
        print("Handling request for api_delete", request.method)
        if request.method == "OPTIONS":
            await self.web.api_send_response(request)
            return

        if request.method != "DELETE":
            print("Method not allowed")
            raise HttpError(request, 501, "Not Implemented")


        filename = request.url[len(request.route.rstrip("*")) - 1:].strip("/")
        print(f"Deleting file: {filename}")

        try:
            os.remove(filename)
            print(f"File {filename} deleted")
        except OSError:
            print(f"Error deleting file: {filename}")
            raise HttpError(request, 500, "Internal error")

        await self.web.api_send_response(request)

    @authenticate(CREDENTIALS)
    async def api_download(self, request):
        print("Handling request for api_download")
        await request.write("HTTP/1.1 200 OK\r\n")

        filename = request.url[len(request.route.rstrip("*")) - 1:].strip("/")
        print(f"Downloading file: {filename}")

        await request.write("Content-Type: application/octet-stream\r\n")
        await request.write(f"Content-Disposition: attachment; filename={filename}\r\n\r\n")
        await send_file(request, filename)


    #@authenticate(CREDENTIALS)
    async def show_content(self,request):
        await request.write(b"HTTP/1.1 200 OK\r\n")

        #await request.write("Content-Type: application/octet-stream\r\n")
        await request.write("access-control-allow-origin: *\r\n\r\n")
        #await send_file(request,self.web.app.STATIC_DIR+'/'+'header_view.html')
        #await send_file(request, self.web.app.STATIC_DIR+'/'+'header.html')

        file_name = request.url.split('?file_name=')[1]
        #html_body = open( self.web.app.STATIC_DIR+ '/'+'show_content.html').read()
        #print('file_name: ',file_name)
        #content = open(file_name).read()
        #html_body = html_body.replace("{{content}}", content)
        #await request.write(html_body)
        #await request.write(content)
        currdir=os.getcwd()
        if currdir=='/': currdir=''
        print(f"show_content: ", currdir, file_name)
        await send_file(
            request,
            '%s/%s' % (currdir, file_name),
        )

        #await send_file(request, self.web.app.STATIC_DIR+ '/footer.html')

    #@authenticate(CREDENTIALS)
    async def upload(self, request):
        print("Handling request for upload")

        if request.method == "OPTIONS":
            await self.web.api_send_response(request)
            return

        if request.method != "PUT":
            print("Method not allowed")
            raise HttpError(request, 501, "Not Implemented")

        bytesleft = int(request.headers.get('Content-Length', 0))
        print(f"Bytes to upload: {bytesleft}")

        if not bytesleft:
            await request.write("HTTP/1.1 204 No Content\r\n\r\n")
            print("No content to upload")
            return

        output_file = request.url[len(request.route.rstrip("*")) - 1:].strip("/")
        tmp_file = output_file + '.tmp'
        print(f"Uploading file to: {tmp_file}")

        try:
            with open(tmp_file, 'wb') as o:
                while bytesleft > 0:
                    chunk = await request.read(min(bytesleft, 64))
                    o.write(chunk)
                    bytesleft -= len(chunk)
                o.flush()
            print(f"File {tmp_file} uploaded")
        except OSError:
            print(f"Error uploading file: {tmp_file}")
            raise HttpError(request, 500, "Internal error")

        try:
            os.remove(output_file)
            print(f"Old file {output_file} removed")
        except OSError:
            pass

        try:
            os.rename(tmp_file, output_file)
            print(f"File {tmp_file} renamed to {output_file}")
        except OSError:
            print(f"Error renaming file: {tmp_file}")
            raise HttpError(request, 500, "Internal error")

        #await self.web.api_send_response(request, 201, "Created")
        return ' ' 

