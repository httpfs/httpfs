import logging


class _FuseLogger:
    """
    Because the default fusepy logger is too verbose
    """
    log = logging.getLogger('fuse.log-mixin')

    def __call__(self, op, path, *args):
        self.log.debug('-> %s %s', op, path)
        ret = '[Unhandled Exception]'
        try:
            ret = getattr(self, op)(path, *args)
            return ret
        except OSError as e:
            ret = str(e)
            raise
        finally:
            if isinstance(ret, Exception):
                self.log.warning('<- %s %s', op, repr(ret))
            else:
                self.log.debug('<- %s', op)
