from machine import UART, Pin, PWM
from time import ticks_ms, ticks_diff, sleep_ms

# Khởi tạo UART0 trên GP0 (TX) và GP1 (RX) với tốc độ baud 9600
uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))
# Khởi tạo PWM trên chân GPIO
servo = PWM(Pin(6))
motor = PWM(Pin(10))
# thiết lập tần số
servo.freq(50)  # Tần số PWM servo 50Hz
motor.freq(20000)  # tần số 20khz
# điều khiển hướng tiến lùi
dir1 = Pin(14, Pin.OUT) 
dir2 = Pin(15, Pin.OUT)
# Hàm đặt góc servo (0-180 độ)
def set_servo_angle(angle):
    # Giới hạn góc từ 0 đến 180
    angle = max(0, min(180, angle))
    # Tính giá trị PWM: 0.5ms (0°) đến 2.5ms (180°)
    pulse_width = (angle / 180) * (2.5 - 0.5) + 0.5  # Độ rộng xung (ms)
    Sduty = int(pulse_width / 20 * 65535)  # Chuyển đổi sang giá trị 16-bit (20ms chu kỳ)
    servo.duty_u16(Sduty)
def set_pwm(pwm):
    pwm = max(0, min(100, pwm)) # giới hạn trong khoảng 0-->100
    Mduty = int((pwm / 100) * 65515)
    motor.duty_u16(Mduty)
set_servo_angle(90)# min 60deg, max 120deg
set_pwm(0)
count = 90
st1 = 0
st2 = 0
last_time = ticks_ms()
while True:
    current_time = ticks_ms()
    if uart.any():  # Kiểm tra dữ liệu trong bộ đệm
        data = uart.read()
        try:
            data_str = data.decode().strip()
            print("Dữ liệu nhận được:", data_str)
            if data_str == 'F':
                dir1.on()
                dir2.off()
                set_pwm(speed)
            elif data_str == 'B':
                dir1.off()
                dir2.on()
                set_pwm(speed)
            elif data_str == 'G':
                dir1.on()
                dir2.off()
                set_pwm(speed)
                st2 = 1
            elif data_str == 'H':
                dir1.on()
                dir2.off()
                set_pwm(speed)
                st1 = 1
            elif data_str == 'I':
                dir1.off()
                dir2.on()
                set_pwm(speed)
                st2 = 1
            elif data_str == 'J':
                dir1.off()
                dir2.on()
                set_pwm(speed)
                st1 = 1
            elif data_str == 'L':
                st2 = 1
            elif data_str == 'R':
                st1 = 1
            elif data_str == '1':
                speed = 0
            elif data_str == '4':
                speed = 65
            elif data_str == '7':
                speed = 80
            elif data_str == '9':
                speed = 100
            else:
                st1 = 0
                st2 = 0
                dir1.off()
                dir2.off()
        except:
            print("Lỗi khi xử lý dữ liệu:", data)           
    if st1 == 1 and ticks_diff(current_time, last_time) >= 30:
        count += 1
        last_time = current_time
    if st2 == 1 and ticks_diff(current_time, last_time) >= 30:
        count -= 1
        last_time = current_time  
    count = max(60, min(count, 120)) 
    set_servo_angle(count)
