# py-Tosha-1

## ESP32 based micro system, for remote control this device
```
This code must be upload to ESP32 chip microPython based 
```
![image info](/doc/01-index.jpg)

другие картинки проекта [Configuration Reference](/doc/images.md)


## Structure code
```

main.py - файл конфигурации этого устройства
list_devices



modules - папка для модулей расширения, каждый модуль это файл или папка принадлежащий(я)
 каждой отдельной единицы внутреннего модуля устройства.
 Каждый модуль работает в постоянном асинхронном цикле 
 Свойство "state"
 {uid:'sensor_dev_15559', name: 'name_of_unit', data:"any data"}
 data - блок инфыормации содержащий произвольные данные

```

libs - папка с библиотеками расширяющих возможности устройства



### Customize configuration
See [Configuration Reference](https:// xxxxxxxxxxxx.xxxxxxxxxxxx.xxxxxxxxxxx /)
