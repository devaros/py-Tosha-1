import network
import uasyncio as asyncio
import ntptime
import json
from .kernel import  Service
import time
import machine

class NetworkManager(Service):
    def __init__(self, name, timezone_offset=0): #, timezone_offset=7
        super().__init__(name)
        self.sta = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        self.timezone_offset = timezone_offset  # Смещение часового пояса в часах
        #ntptime.NTP_DELTA = ntptime.NTP_DELTA - self.timezone_offset * 3600  # Корректировка таймзоны

    async def connect_to_network(self, *args):
        if args:
          d = {"ssid":args[0], "pswd":args[1]}
        else:

          if self.sta.isconnected():
            print('already connected')
            print(self.sta.ifconfig())
            return True

          print('Start connection')

          # Активация интерфейса STA (клиентский режим)
          self.sta.active(True)

          try:
            with open('/wifi.json', 'r') as f:
              d = json.loads(f.read())
              #f.close()
          except Exception as e:
            print(f"Failed to open file wifi.json")
            return False
        #self.ssid = d.get('ssid')
        #self.pswd = d.get('pswd')
        if d.get('ssid') and d.get('pswd'):
          self.sta.disconnect()
          self.sta.connect(d.get('ssid'), d.get('pswd'))

        #await asyncio.sleep(3)
        for _ in range(5): 
            #await asyncio.sleep(3)
            time.sleep(3)
            if self.sta.isconnected():
                #self.state['ssid'] = self.sta .config('ssid')
                #self.state['isconnected'] = self.sta.isconnected()
                print('connected', self.sta.ifconfig())
                # Отключение точки доступа для экономии энергии
                self.ap.active(False)

                if args:
                  ds = json.dumps(d, separators=(",\r\n", ":"))
                  with open('/wifi.json', 'w') as f:
                    f.write(ds)
                return True

            #await asyncio.sleep(2)
            #self.sta.connect(d.get('ssid'), d.get('pswd'))  # Попробовать подключиться в течение интервала
            #self.connect( save=False)
            print('. ', end='')
        self.sta.disconnect()
        #self.sta.active(False)
        print('can`t connect')
        self.ap.active(True)
        return False

    def connect(self, *args, save=True):
        #self.sta.connect(kwargs.get('ssid'), kwargs.get('pswd'))
        #self.sta.connect(*args)

        #asyncio.run( self.connect_to_network(*args) )
        asyncio.create_task(self.connect_to_network(*args))

        #print('connected -4')
        #asyncio.create_task( self.connect_to_network(*args) )
        #_ = 
        #loop = asyncio.get_event_loop()
        #loop.create_task(self.connect_to_network(*args))


    def forget(self):
        ds = json.dumps({})
        with open('/wifi.json', 'w') as f:
            f.write(ds)

        async def forgot():
          await asyncio.sleep(2)
          self.sta.disconnect()
          print("Net forgot" )
          await self.connect_to_network()

        asyncio.create_task(forgot())


    def create_access_point(self):
        # Создание точки доступа
        self.ap.active(True)
        self.ap.config(essid='py-Tosha', password='12345678')

    async def sync_time(self):
        try:
            # Проверяем подключение к сети перед синхронизацией времени
            if not self.sta.isconnected():
                print("Not connected to network, cannot sync time")
                return

            # Синхронизация времени через NTP
            ntptime.settime()  # С учётом ранее скорректированного NTP_DELTA
            rtc=machine.RTC()
            #(year, month, day, hours, minutes, seconds,  weekday, yearday) = ntptime.gmtime()
            (year, month, day, hours, minutes, seconds, weekday, yearday) = time.gmtime(time.time()+self.timezone_offset*3600)
#(year, month, day, hours, minutes, seconds, weekday, yearday)
            rtc.datetime((year, month, day, 0, hours, minutes, seconds, 0) )
            #rtc.datetime(time.gmtime(time.time()+self.timezone_offset*3600))

            print("NTP time synced: ", time.localtime())
        except Exception as e:
            print(f"Failed to sync time: {e}")

    async def check_time(self):
        while True:
            year = time.localtime()[0]  # Проверка текущего года
            #if year < 2022:
            await self.sync_time()
            await asyncio.sleep(3600*11)  # Проверять с периодом час * X часов

    async def reconnect(self):
        while True:
          if not self.sta.isconnected() and not self.ap.status('stations'):
            await self.connect_to_network()
          await asyncio.sleep(60*30)  # Проверять с периодом мин * X часов


    async def run(self):
        await asyncio.sleep(3)

        #for _ in range(3):  # try reconnect
            #await self.connect_to_network()
            #await asyncio.sleep(3*60)

        # Создание точки доступа, если не удалось подключиться к известным сетям
        if not await self.connect_to_network():
            self.create_access_point()
            return

        #if not self.ap.status('stations'): # Переподключаемся если нет клиентов
           
        asyncio.create_task(self.reconnect()) # Отслеживаем соединение
        

        # Синхронизация времени после успешного подключения
        #await asyncio.sleep(5)
        #year = time.localtime()[0]  # Проверка текущего года
        #if year < 2022:
            #await self.sync_time()

        await asyncio.sleep(5)
        # Запуск задачи для периодической проверки времени
        asyncio.create_task(self.check_time())

    @property
    def status__old2(self):
      return self.sta.isconnected(), self.sta .config('ssid')
      

    def get_status(self):
        # Возвращение статуса подключения и конфигурации сети
        return {
            "connected": self.sta.isconnected(),
            "ssid": self.sta .config('ssid'),
            "ifconfig": self.sta.ifconfig() if self.sta.isconnected() else None
        }
