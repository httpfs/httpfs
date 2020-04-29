"""
Contains a class for modifying the default FUSE logger
"""

import logging


class _FuseLogger:
    """
    Because the default fusepy logger is too verbose
    """
    log = logging.getLogger('fuse.log-mixin')

    def __call__(self, operation, path, *args):
        self.log.debug('-> %s %s', operation, path)
        ret = '[Unhandled Exception]'
        try:
            ret = getattr(self, operation)(path, *args)
            return ret
        except OSError as exception:
            ret = str(exception)
            raise
        finally:
            if isinstance(ret, Exception):
                self.log.warning('<- %s %s', operation, repr(ret))
            else:
                self.log.debug('<- %s', operation)
