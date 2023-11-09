import threading
from simulators.PIR.pir import simulated_pir


def run_RPIR1(settings, threads, stop_event, print_lock):

    pir_name = settings['name']

    if settings['simulated']:
        pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        from sensors.PIR.DPIR1 import real_pir
        pin = settings['pin']
        pir_thread = threading.Thread(target=real_pir, args=pin)
        pir_thread.start()
        threads.append(pir_thread)


def run_RPIR2(settings, threads, stop_event, print_lock):

    pir_name = settings['name']

    if settings['simulated']:
        pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        from sensors.PIR.RPIR2 import real_pir
        pin = settings['pin']
        pir_thread = threading.Thread(target=real_pir, args=pin)
        pir_thread.start()
        threads.append(pir_thread)


def run_DPIR1(settings, threads, stop_event, print_lock):
    pir_name = settings['name']

    if settings['simulated']:
        pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        from sensors.PIR.DPIR1 import real_pir
        pin = settings['pin']
        pir_thread = threading.Thread(target=real_pir, args=pin)
        pir_thread.start()
        threads.append(pir_thread)


def run_DS1(settings, threads, stop_event, print_lock):
    pir_name = settings['name']

    if settings['simulated']:
        pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        from sensors.PIR.DS1 import real_pir
        pin = settings['pin']
        pir_thread = threading.Thread(target=real_pir, args=pin)
        pir_thread.start()
        threads.append(pir_thread)