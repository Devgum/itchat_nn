# coding:utf-8

def reply_func(func_list):
    def decorator(func):
        func_list.append(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        return wrapper
    return decorator