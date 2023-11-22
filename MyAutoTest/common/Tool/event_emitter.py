class EventEmitter:
    """
    回调函数应用示例，无实际应用
    """
    def __init__(self):
        self.callbacks = []

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def trigger_event(self, message):
        for callback in self.callbacks:
            callback(message)


def callback_function(message):
    print("Received message:", message)



event_emitter = EventEmitter()
event_emitter.register_callback(callback_function)
event_emitter.trigger_event("Hello, World!")