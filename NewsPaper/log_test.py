import logging

logger = logging.getLogger('django')
request_logger = logging.getLogger('django.request')
security_logger = logging.getLogger('django.security')

print("\n=== Тест логирования запущен ===\n")

logger.debug("Это DEBUG сообщение (должно появиться только в консоли при DEBUG=True)")
logger.info("Это INFO сообщение (должно попасть в general.log при DEBUG=False)")
logger.warning("Это WARNING сообщение (в консоли + general.log при DEBUG=False)")
logger.error("Это ERROR сообщение (в errors.log, general.log и на email при DEBUG=False)")
logger.critical("Это CRITICAL сообщение (в errors.log и на email при DEBUG=False)")

request_logger.error("Ошибка в django.request (должна попасть в errors.log и на email)")
security_logger.warning("Security warning! Это сообщение должно попасть в security.log")

print("\n=== Тест логирования завершён ===\n")
