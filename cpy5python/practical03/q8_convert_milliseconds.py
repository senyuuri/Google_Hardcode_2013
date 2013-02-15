#Name:q8_convert_milliseconds.py
#Author:Zhan Yuli
#Description:Converting milliseconds to hours, minutes, and seconds
#Created:150213

def convert_ms(n):
    h = int(n/1000/60/60)
    m = int((n-h*3600000)/1000/60)
    s = int((n - h*3600000 - m*60000)/1000)
    print("{0:d}:{1:d}:{2:d}".format(h,m,s))

convert_ms(5500)
convert_ms(100000)
convert_ms(555550000)
