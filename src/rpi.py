
#!/usr/bin/env python3

import time, requests, math, json

import unicornhat as unicorn
import subprocess






unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()



try:
    while True:
        r = requests.get('http://webster.inf.ed.ac.uk:5001/api/status')

        

        if r.status_code == 200:
            status = r.json()

            

            mem_usage = float(status['utilization.memory [%]'])/100
            usage = float(status['utilization.gpu [%]'])/100
            temp = (float(status['temperature.gpu'])-40)/40

            print(mem_usage, usage, temp)
            
            mem_col = (0,255,0) if mem_usage < 0.5 else (255,170,0) if mem_usage < 0.85 else (255,0,0)
            unicorn.set_pixel(0,0,*mem_col)
            mem_usage_width = int(round(mem_usage*(width-1)))
            for x in range(mem_usage_width):
                unicorn.set_pixel(x,0,*mem_col)


            use_col = (0,255,0) if mem_usage < 0.5 else (255,170,0) if mem_usage < 0.85 else (255,0,0)
            unicorn.set_pixel(0,1,*use_col)
            usage_width = int(round(usage*(width-1)))
            for x in range(usage_width):
                unicorn.set_pixel(x,1,*use_col)

            
            temp_col = (0,255,0) if temp < 0.5 else (255,170,0) if temp < 0.85 else (255,0,0)
            unicorn.set_pixel(0,2,*temp_col)
            temp_width = int(round(temp*(width-1)))
            for x in range(temp_width):
                unicorn.set_pixel(x,2,*temp_col)

            unicorn.set_pixel(width-1, height-1, 0,0,100)

        else:
            unicorn.set_pixel(width-1, height-1, 100,0,0)

        unicorn.show()

        curr_ips = subprocess.call(["hostname", "-I"])

        r = requests.get('http://mckenzie.tomhosking.co.uk/index.py/api/ip_responder?node=pizero&ip={:}'.format(curr_ips))


        time.sleep(10)

except Exception as e:
    print(e)
    print('Exiting...')