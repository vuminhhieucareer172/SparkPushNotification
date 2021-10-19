from unidecode import unidecode


def generate_job_id(name: str):
    res = unidecode(name).lower().strip()
    return '_'.join(res.split())
