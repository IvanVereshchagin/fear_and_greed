import logging 

logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename='./app/logging/signup.log')
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s %(password)s %(username)s %(email)s %(role)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
