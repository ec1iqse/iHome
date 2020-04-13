# Note
1. 运行celery命令：
~~~bash
celery -A iHome.tasks.task_sms  worker -l info
~~~
    
***注意！***

celery运行时的目录必须跟verify_code中导入的send_sms路径一致！