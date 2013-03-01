# import hotshot
# import os
# import time
# import settings
# import tempfile

# try:
#     PROFILE_LOG_BASE = settings.PROFILE_LOG_BASE
# except:
#     PROFILE_LOG_BASE = tempfile.gettempdir()


# def profile(log_file):
#     """Profile some callable.

#     This decorator uses the hotshot profiler to profile some callable (like
#     a view function or method) and dumps the profile data somewhere sensible
#     for later processing and examination.

#     It takes one argument, the profile log name. If it's a relative path, it
#     places it under the PROFILE_LOG_BASE. It also inserts a time stamp into the
#     file name, such that 'my_view.prof' become 'my_view-20100211T170321.prof',
#     where the time stamp is in UTC. This makes it easy to run and compare
#     multiple trials.
#     """

#     if not os.path.isabs(log_file):
#         log_file = os.path.join(PROFILE_LOG_BASE, log_file)

#     def _outer(f):
#         def _inner(*args, **kwargs):
#             # Add a timestamp to the profile output when the callable
#             # is actually called.
#             (base, ext) = os.path.splitext(log_file)
#             base = base + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())
#             final_log_file = base + ext

#             prof = hotshot.Profile(final_log_file)
#             try:
#                 ret = prof.runcall(f, *args, **kwargs)
#             finally:
#                 prof.close()
#             return ret

#         return _inner
#     return _outer


# def servercache(argsfunc=None):
#     def _outer(func):
#         def _inner(request, *args, **kwargs):
#             request._server_cache = {}
#             request._server_cache['argsfunc'] = argsfunc
#             return func(request, *args, **kwargs)
#         return _inner
#     return _outer

from functools import wraps


def servercache(argsfunc=None):
    def outer_decorator(func):
        def inner_decorator(request, *args, **kwargs):
            request._server_cache = {}
            request._server_cache['argsfunc'] = argsfunc
            return func(request, *args, **kwargs)
        return wraps(func)(inner_decorator)
    return outer_decorator
