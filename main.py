import gc
import machine as m
from machine import reset
from libs.kernel import os_kernel , Kernel, Service, load
from libs.ble_connect import ble
from libs.ble_repl import ble_repl
from libs.net_manager import NetworkManager
from modules.switches import SwitchesBoard  # переключатели
from web.webserver import WebServer
from web.files import Files  # Файловый менеджер 
from web.web_switches import WebSwitches 
from web.web_cron import WebCron

from web.net_configure import NetConfig 
from modules.cron import CronScheduler
#import webrepl
#webrepl.start()  #port 8266

net = None
sw = None
cron = None

list_devs =[11,22]

h = "h.ble, h.net, h.web, dev_list, reset, ..."

class init( ):
    #def __init__(self):
        global net, sw, cron
        #self.os_kernel = Kernel()

        # Инициализация сетевого менеджера
        net = NetworkManager(name='NET_MANAGER', timezone_offset=7)
        os_kernel.add_task(net)

        sw = SwitchesBoard(name="Switches Board")
        os_kernel.add_task(sw)

        # Инициализация веб-интерфейса
        web = WebServer(name="WebServer", kernel=os_kernel)
        #self.web.devs = self.devs
        os_kernel.add_task(web)

        # Инициализация файлового веб-интерфейса
        _ = Files(name="Web file manager", web=web)

        # Инициализация web-интерфейса переключателей
        _ = WebSwitches(name="Web switches", web=web)

        # Инициализация web-интерфейса конфигуратора сети
        _ = NetConfig(name="Network Manager", web=web, net_manager=net)

        _ = WebCron(name="Web cron", web=web)


        cron = CronScheduler()
        os_kernel.add_task(cron)

        cron.append_command( 22,  sw.set_value, 'Включить выход', (8, 1))
        cron.append_command( 11,  sw.set_value, 'Отключить выход', {"id":7, "value":0} )

        #print("Starting OS Kernel")
        os_kernel.start()


if __name__ == "__main__":
    init()
    print('type h for help')
    print('free_mem: ',gc.mem_free())
