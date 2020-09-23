# import logging
#
#
# class NugflowFormatter(logging.Formatter):
#     def __init__(self):
#         super().__init__(("%(levelname)s | " "%(name)s:L%(lineno)d | " "%(message)s"))
#
#
# handler = logging.StreamHandler()
# handler.setFormatter(NugflowFormatter())
#
#
# def get_logger(name: str) -> logging.Logger:
#     logger = logging.getLogger(name)
#     logger.addHandler(handler)
#     logger.setLevel(logging.DEBUG)
#     return logger
