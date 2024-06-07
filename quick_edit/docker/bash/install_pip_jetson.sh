python3 -m pip install --upgrade pip
pip3 install --ignore-installed --upgrade --no-deps numpy wheel setuptools grpcio-tools \
    attrdict attrdict pandas tqdm matplotlib seaborn requests\
     pydot utm pyyaml tqdm seaborn viztracer flask flask_cors  \
      diskcache icecream psutil py-cpuinfo ipympl ultralytics onnx fiftyone thop jupyter notebook
pip3 install --no-deps scikit-image albumentations
pip install git+https://media_manager:glpat-FQPEDyrPz5SfbsbMyMfy@gitlab.tsn.tno.nl/intelligent_imaging/python/pipeli
nes/media_manager.git --no-deps
run pip3 install git+https://dlutils_ii:glpat-EQCGEC3FjaXctPnr6jQt@gitlab.tsn.tno.nl/intelligent_imaging/python/deep_lea
rning/dlutils_ii.git --no-deps
run pip3 install git+https://yolo-plugins:glpat-_nNxVBRgSd7A_9Ae5rtz@gitlab.tsn.tno.nl/intelligent_imaging/python/deep_learning/yolo-plugins.git --no-
rning/dlutils_ii.git --no-deps
run pip3 install git+https://yolo-plugins:glpat-_nNxVBRgSd7A_9Ae5rtz@gitlab.tsn.tno.nl/intelligent_imaging/python/deep_learning/yol
o-plugins.git --no-deps
pip3 install git+https://videosets_ii:glpat-Fns9WB-uccyz-pcuPXdx@gitlab.tsn.tno.nl/intelligent_imaging/python/data_management/v
ideosets_ii.git --no-deps
run pip3 install git+https://engine_utils:glpat-JxAViWcA7f2ikj3A1YGS@gitlab.tsn.tno.nl/intelligent_imaging/python/pipelines/engine_
utils.git --no-deps

RUN git clone https://toolboxes:glpat-zcSeCzRLLpdyxy_5NUhE@gitlab.tsn.tno.nl/intelligent_imaging/python/toolboxes.git  && \
    pip3 install --no-deps ./toolboxes/motiontoolbox && \
    pip3 install --no-deps ./toolboxes/bboxtoolbox && \
    pip3 install --no-deps ./toolboxes/trackertoolbox && \
    pip3 install --no-deps ./toolboxes/geotoolbox && \
    rm -rf toolbox
# install rda_videoserver
RUN git clone https://v4r_tools:glpat-mFvYDgz8-fWZ3B1j3xJx@gitlab.tsn.tno.nl/intelligent_imaging/python/pipelines/v4r_tools.git &&
\
    pip3 install ./v4r_tools/rda_videoserver --no-deps && \
    pip3 install ./v4r_tools/rda_modules  --no-deps && \
    rm -rf  v4r_tools
ADD fix_packages.py .
RUN python3 fix_packages.py
RUN sed -i '8d' /usr/local/lib/python3.10/dist-packages/albumentations/augmentations/__init__.py
RUN mkdir /root/rda/ && cd /root/rda && ln -s /root/git/mantis/rda/modules modules