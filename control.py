from pynput import keyboard
#import threading
import serial
import time

# Cấu hình cổng COM
ser = serial.Serial('COM36', 115200, timeout=1)# thay đổi COM36 đúng với cổng COM của bạn
time.sleep(2)# Đợi 2s

digits = ['0','4','7','9']
set_keys = set()# ngăn không cho quá trình gửi lặp lại(chỉ 1 lần khi nhấn giữ là đủ) 
def hold_keys():
    if keyboard.Key.up in set_keys:
        #ser.write(b'F')
        print(f'đang giữ: up')
    elif keyboard.Key.down in set_keys:
        #ser.write(b'B')
        print(f'đang giữ: down')
    else:
        ser.write(b'S')# dừng lại khi nhả phím up or down
def on_press(key):
    try:
        if key not in set_keys:
            set_keys.add(key)
            if hasattr(key, 'char') and key.char is not None and key.char in digits:# xử lí riêng các phím key.char có trong danh sách digits 
                ser.write(key.char.encode())
                print(f'Speed:{key.char} (0->4->7->9)')
            elif key == keyboard.Key.up:
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
    except:
        print(f'err')    
# khi nhả phím
def on_release(key):
    if key in set_keys:
        set_keys.discard(key)
        print(f'Đã nhả: {key}')
        if key == keyboard.Key.left:
            ser.write(b'l')# gửi lệnh dừng rẽ trái 
        elif key == keyboard.Key.right:
            ser.write(b'r')# gửi lệnh dừng rẽ phải
    hold_keys()
    # nhấn esc để thoát
    if key==keyboard.Key.esc:
        ser.close()# Ngắt kết nối cổng serial
        return False # dừng listener
# lắng nghe bàn phím
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()