from pynput import keyboard
#import threading
import serial
import time

# Cấu hình cổng COM
ser = serial.Serial('COM36', 115200, timeout=1)
time.sleep(2)# Đợi 2s

#key = keyboard.read_key()
#print(f"bạn đã nhấn:{key}")
digits = ['0','4','7','9']
#valid_keys = [keyboard.KeyCode.from_char(d) for d in digits]
def on_press(key):
    try:       
        if key.char in digits:
            cmd = key.char
            ser.write(cmd.encode())
            print(f'Speed:{key.char} (0->4->7->9)')
    except AttributeError:
        if key == keyboard.Key.up:
            ser.write(b'F')
            print(f'đã nhấn: up')
        elif key == keyboard.Key.down:
            ser.write(b'B')
            print(f'đã nhấn: down')
        elif key == keyboard.Key.left:
            ser.write(b'L')
            print(f'đã nhấn: left')
        elif key == keyboard.Key.right:
            ser.write(b'R')
            print(f'đã nhấn: right') 
    time.sleep(0.01)# 10ms     
    #except AttributeError:
        #print(f"{key} không phải lệnh gửi")

def on_release(key):
    ser.write(b'S')# Gửi S để dừng(không tự lặp lại)
    print(f'Đã gửi:S')
    if key==keyboard.Key.esc:# Ngắt kết nối cổng serial, thoát toàn bộ
        ser.close()
        return False # dừng listener
# lắng nghe bàn phím
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()