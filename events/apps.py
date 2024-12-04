from django.apps import AppConfig
import schedule
import time
from django.core.management import call_command
from threading import Thread


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        def run_scraper():
            # print("abc")
            call_command("scrapping")
        schedule.every(5).seconds.do(run_scraper)

        def scheduler_thread():
            while True:
                schedule.run_pending()
                time.sleep(1)
        scheduler_thread = Thread(target=scheduler_thread)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
