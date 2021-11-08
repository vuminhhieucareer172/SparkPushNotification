from psutil import NoSuchProcess
import psutil


def is_process_running(pid, detail: str = ''):
    """ Check For the existence of a unix pid. """
    try:
        process = psutil.Process(pid)
        return detail in ' '.join(process.cmdline())
    except NoSuchProcess:
        return False
