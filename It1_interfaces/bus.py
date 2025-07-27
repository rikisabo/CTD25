
_listeners: dict[str, list] = {}

def subscribe(topic: str, fn):
    _listeners.setdefault(topic, []).append(fn)

def publish(topic: str, data=None):
    for fn in _listeners.get(topic, []):
        fn(data)
