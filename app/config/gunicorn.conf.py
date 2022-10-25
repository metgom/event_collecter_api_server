daemon = True
bind = "0.0.0.0:5000"
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "./log/access.log"
errorlog = "./log/error.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s %(M)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

