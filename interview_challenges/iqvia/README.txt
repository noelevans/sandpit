To run the unittests:

$ py.test test_contact_manager.py
$ py.test test_contact_model.py

(the default pytest invocation hits problems as there is a folder - part_1 -
showing the working to complete step 1)


To run the celery process in full, open terminals with each of these commands:

$ python contact_manager.py
$ celery -A auto_generation_worker worker --concurrency=1 --loglevel=info
$ python auto_generation_master.py

View results at:
    http://127.0.0.1:5000/api/get_all/user


Note that the celery worker has the setting --concurrency=1 forcing a single 
thread to be used to execute the create and delete command. This is necessary 
as explained here:

https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#threading-pooling-behavior



I tend to use conda rather than pip env. I imagine requirements.txt 
could be a lot smaller.

Please email if there are any questions: noelevans@gmail.com

Thanks, Noel
