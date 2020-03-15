
#!/usr/bin/env python3

import time, requests, math, json

import unicornhat as unicorn
import subprocess, os






unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()



try:
    MCKENZIE_PROXY = os.environ['MCKENZIE_PROXY']

    while True:
        r = requests.get(MCKENZIE_PROXY + '/api/get')

        

        if r.status_code == 200:
            status = r.json()

            print(status)

            if len(status['running_progress']) > 1:
                for y, prog in enumerate(status['running_progress'][:3]):
                    width = int(round(prog/100*(width-1)))
                    prog_col = (255,170,0)
                    for x in range(width):
                        unicorn.set_pixel(x,y,*prog_col)

            num_errs = status['count_errors']

            temp_col = (255,0,0)
            err_width = min(width-2, num_errs)
            for x in range(err_width):
                unicorn.set_pixel(x,4,*temp_col)

            unicorn.set_pixel(width-1, height-1, 0,0,100)

        else:
            unicorn.set_pixel(width-1, height-1, 100,0,0)

        unicorn.show()

        curr_ips = subprocess.check_output(["hostname", "-I"])

        r = requests.get(MCKENZIE_PROXY + '/api/ip_responder?node=pizero&ip={:}'.format(curr_ips))


        time.sleep(10)

except Exception as e:
    print(e)
    print('Exiting...')