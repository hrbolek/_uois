from prometheus_client import make_asgi_app, Summary

def collectTime(metricprefix):
    s = Summary(f'{metricprefix}_processing_seconds', f'{metricprefix}_time_spent')

    def decorator(f):
        @s.time()
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated
    return decorator

prometheusClient = make_asgi_app