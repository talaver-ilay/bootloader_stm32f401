import hid

def connect(vid,pid,self):
    try:
        self.myDevice = hid.Device(vid = vid, pid = pid) # подключиться к устройству
    except:
        self.add_item("None Device!")

def send_bin(self):
    size64 = len(self.obj.file_list)
    for i in range(size64):
        print(i)
        self.progress_signal.emit(i*64)                       # обнавить полоску загрузки
        self.obj.myDevice.write(bytes(self.obj.file_list[i])) # отправка 64 байт данных


# while True:
#     rdata = mydevice.read(32)
#     for data in rdata:
#         print(data)