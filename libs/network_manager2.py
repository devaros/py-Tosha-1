import network
import uasyncio as asyncio
import ntptime
import json
#from .kernel import Kernel, Service
import time
import machine

class NetworkManager(Service):
    def __init__(self, name, timezone_offset=7):
        super().__init__(name, None)
        self.sta_if = network.WLAN(network.STA_IF)
        self.ap_if = network.WLAN(network.AP_IF)
        self.timezone_offset = timezone_offset  # Смещение часового пояса в часах
        #ntptime.NTP_DELTA = ntptime.NTP_DELTA - self.timezone_offset * 3600  # Корректировка таймзоны

    async def connect_to_network(self):
        print('Start connection')
        if self.sta_if.isconnected():
            print('already connected')
            print(self.sta_if.ifconfig())
            return True

        # Отключение точки доступа для экономии энергии
        self.ap_if.active(False)

        # Активация интерфейса STA (клиентский режим)
        self.sta_if.active(True)
        f = open('objects/wifi.json', 'r')
        d = json.loads(f.read())
        self.ssid = d.get('ssid')
        self.pswd = d.get('pswd')
        self.sta_if.connect(self.ssid, self.pswd)

        for _ in range(10):  # Попробовать подключиться в течение 10 секунд
            if self.sta_if.isconnected():
                print('connected', self.sta_if.ifconfig())
                return True
            await asyncio.sleep(1)
            print('cant connect 10 sec')
        return False

    def create_access_point(self):
        # Создание точки доступа
        self.ap_if.active(True)
        self.ap_if.config(essid='ESP32_AP', password='password123')

    async def sync_time(self):
        try:
            # Проверяем подключение к сети перед синхронизацией времени
            if not self.sta_if.isconnected():
                print("Not connected to network, cannot sync time")
                return

            # Синхронизация времени через NTP
            ntptime.settime()  # С учётом ранее скорректированного NTP_DELTA
            rtc=machine.RTC()
            rtc.datetime(time.gmtime(time.time()+self.timezone_offset*3600))

            print("NTP time synced")
        except Exception as e:
            print(f"Failed to sync time: {e}")

    async def check_time(self):
        while True:
            year = time.localtime()[0]  # Проверка текущего года
            if year < 2022:
                await self.sync_time()
            await asyncio.sleep(86400)  # Проверять раз в сутки

    async def run(self):
        if not await self.connect_to_network():
            # Создание точки доступа, если не удалось подключиться к известным сетям
            self.create_access_point()
            return

        # Синхронизация времени после успешного подключения
        year = time.localtime()[0]  # Проверка текущего года
        if year < 2022:
            await self.sync_time()

        # Запуск задачи для периодической проверки времени
        asyncio.create_task(self.check_time())

    async def get_status(self):
        # Возвращение статуса подключения и конфигурации сети
        return {
            "connected": self.sta_if.isconnected(),
            "ifconfig": self.sta_if.ifconfig() if self.sta_if.isconnected() else None
        }
