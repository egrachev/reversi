# -*- coding: utf-8 -*-


from datetime import datetime


class Logger(object):
    def __init__(self, log_impl):
        self.log_impl = log_impl

    def log(self, message):
        raise NotImplementedError()


class ConsoleLogger(Logger):
    def __init__(self, log_impl):
        super(ConsoleLogger, self).__init__(log_impl)

    def log(self, message):
        self.log_impl.console_log(message)


class FileLogger(Logger):
    def __init__(self, log_impl):
        super(FileLogger, self).__init__(log_impl)
        self.file = open('game.log', mode='w+')

    def log(self, message):
        self.log_impl.file_log(self.file, message)


class LoggerImpl(object):
    def console_log(self, message):
        raise NotImplementedError()

    def file_log(self, file_obj, message):
        raise NotImplementedError()


class ShortTimeFormatLoggerImpl(LoggerImpl):
    def __init__(self):
        self.format = '%H:%M:%S'

    def console_log(self, message):
        print('[%s] %s' % (datetime.now().strftime(self.format), message))

    def file_log(self, file_obj, message):
        file_obj.write('[%s] %s\n' % (datetime.now().strftime(self.format), message))


class FullTimeFormatLoggerImpl(LoggerImpl):
    def __init__(self):
        self.format = '%Y.%m.%d %H:%M:%S'

    def console_log(self, message):
        print('[%s] %s' % (datetime.now().strftime(self.format), message))

    def file_log(self, file_obj, message):
        file_obj.write('[%s] %s\n' % (datetime.now().strftime(self.format), message))



logger = FileLogger(FullTimeFormatLoggerImpl())
