
import threading
import requests

from aiolimiter import AsyncLimiter
import random
import time
from flask import Flask
import asyncio
import logging

j=0
start=0

logging.basicConfig(
    filename="client.log",
    format="Date-Time : %(asctime)s - %(levelname)s -  Line No. : %(lineno)d - Messages. :%(message)s -Filename: %(filename)s ",
    level=logging.INFO,
)
# # Gets or creates a logger
logger = logging.getLogger(__name__)

app=Flask(__name__)
limiter=AsyncLimiter(max_rate= 500,time_period= 1)
class GuiClient:
    def __init__(self):
        self.add_end_points()
        threading.Thread(
            target=lambda: app.run(
                host="127.0.0.1",
                port=4003,
                debug=True,
                use_reloader=False,
            )
        ).start()

    def add_end_points(self):
        app.add_url_rule(
            "/settings/<action_name>",
            methods=["POST"],
            view_func=self.handle_settings_request,
        )

    def handle_settings_request(self):
        pass

    async def send_data(self,i):
        
        async with limiter:
            global j
            if j==0:
                global start
                start=time.time()
                j+=1
            #logger.info(f"{i:>2d}: Drip! {(time.time() - ref):>f}  current  :{time.time():>f}  ref: {ref:>f}")
            response = requests.post("http://127.0.0.1:4004/data/",json={"dia":random.uniform(1,100),"inner":random.uniform(200,300),"core":random.uniform(400,500)})
            


object=GuiClient()

run_the_function=[object.send_data(i) for i in range(30000)]
# ref=time.time();asyncio.run(asyncio.wait(run_the_function))

ref=time.time()
asyncio.wait(run_the_function)

logger.info(f"Total time :{time.time()-start}")




#Don't go for while loop.
# i=0
# while i<10: run_the_function=[object.send_data(i)]
#     i+=1
#     if i==10: i=0
#     ref=time.time();asyncio.run(asyncio.wait(run_the_function))
