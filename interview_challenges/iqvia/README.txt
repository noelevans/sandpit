To run the unittests:

$ py.test test_contact_manager.py

(the default pytest invocation hits problems as there is a folder - part_1 -
showing the working to complete step 1)


To run the celery process in full, open terminals with each of these commands:

$ python contact_manager.py   # Run webserver
$ celery -A auto_generation_worker worker --loglevel=info  # Run celery worker
$ python auto_generation_master.py  # Celery master

I tend to use conda rather than pip env. I imagine requirements.txt 
could be a lot smaller.

Please email if there are any questions: noelevans@gmail.com

Thanks, Noel
