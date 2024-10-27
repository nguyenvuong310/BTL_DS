FROM python:3.13
RUN pip3 install "dask[distributed]" "dask" "bokeh>=3.1.0"

