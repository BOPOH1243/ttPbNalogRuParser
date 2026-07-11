import time
from datetime import datetime
from app.parser import fetch
from app.mq.kafka import send_kafka
from app.mq.rabbit import send_status

async def process_search(search_string):
    start = time.time()
    try:
        data = await fetch(search_string)
        duration = round(
            time.time()-start,
            2
        )
        collect_time = str(
            datetime.now()
        )
        total = 0
        # отправка атомарных сообщений Kafka
        for person in data:
            for org in person.get("orgs", []):
                total += 1
                message = {
                    "request":{
                        "search_string":
                            search_string
                    },
                    "response":{
                        "success":True,
                        "error":None,
                        "duration":
                            duration,
                        "collect_time":
                            collect_time,
                        "total":
                            total,
                        "person":{
                            k:v
                            for k,v in person.items()
                            if k!="orgs"
                        },

                        "organization":org
                    }
                }
                await send_kafka(message)
        status = {
            "request":{
                "search_string":
                    search_string
            },
            "response":{
                "success":True,
                "error":None,
                "duration":
                    duration,
                "collect_time":
                    collect_time,
                "total":
                    total,
                "data":data
            }
        }
        await send_status(status)
        return status


    except Exception as e:
        return {
            "request":{
                "search_string":
                    search_string
            },
            "response":{
                "success":False,
                "error":str(e)
            }
        }