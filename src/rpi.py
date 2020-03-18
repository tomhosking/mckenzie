
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

    unicorn.brightness(0.6)
    print('Brightness: ', unicorn.get_brightness())

    while True:
        try:
            r = requests.get(MCKENZIE_PROXY + '/api/get')

            
            unicorn.clear()
            if r.status_code == 200:
                status = r.json()

                print(status)

                counter = 0
                if len(status['running_progress']) > 0:
                    for y, prog in enumerate(status['running_progress'][:3]):
                        prog_width = max(int(round(float(prog)/100*(width-1))), 1)
                        prog_col = (255,170,0)
                        # unicorn.set_pixel(0,y,*prog_col)
                        # print(y, width)
                        for x in range(prog_width):
                            unicorn.set_pixel(x,y,*prog_col)
                        counter +=1
                else:
                    unicorn.set_pixel(0,0, 0,255,0)

                for y in range(counter, min(counter+int(status['count_waiting']), 3)):
                    # print(counter, int(status['count_waiting']), min(counter+int(status['count_waiting']), 4), y)
                    unicorn.set_pixel(0,y, 0,0,200)

                
                if counter is 0 and int(status['count_waiting']) == 0:
                    unicorn.set_pixel(0,0, 0,255,0)

                num_errs = status['count_errors']

                err_col = (255,0,0)
                err_width = min(width-2, num_errs)
                for x in range(err_width):
                    unicorn.set_pixel(x,3,*err_col)

                # unicorn.set_pixel(width-1, height-1, 100,0,100)

            else:
                unicorn.set_pixel(width-1, height-1, 100,0,100)
        catch:
            unicorn.set_pixel(width-1, height-1, 100,0,100)

        unicorn.show()

        curr_ips = subprocess.check_output(["hostname", "-I"])

        try:
            r = requests.get(MCKENZIE_PROXY + '/api/ip_responder?node=pizero&ip={:}'.format(curr_ips))
        catch:
            print('Error connecting to IP responder')


        time.sleep(10)

except Exception as e:

    unicorn.clear()
    unicorn.show()
    print(e)
    print('Exiting...')