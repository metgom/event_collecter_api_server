import uvicorn


daemon = True
bind = "0.0.0.0:5000"
worker_class = uvicorn.workers.UvicornWorker
accesslog = ".log/access.log"
errorlog = ".log/error.log"
