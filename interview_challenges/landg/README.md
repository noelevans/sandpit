# Submission of Noel Evans due 20 October

There are two solutions:
- censor.py and
- censor_serial.py

Each with corresponding tests. I started with a linear solution which assumed there might be extremely long lines which would therefore be handled better with generators across each line of the file.

I am imagining the prose files will be longer rather than wider so it the multiprocessing of censor.py will be more performant.

The files have been formatted with PSF's Black tool. The tests run with `pytest`.
