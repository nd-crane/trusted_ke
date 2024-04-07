### ASP Setup

Github: https://github.com/lyutyuh/ASP

Paper: https://arxiv.org/pdf/2210.14698.pdf

1. Clone the github: git clone git@github.com:lyutyuh/ASP.git

2. Clone nvidia-apex: git clone https://github.com/NVIDIA/apex

Current steps taken with asp environment:\
6. Create a conda virtual environment from the environment.yml file
7. Install pandas
9. conda install -c nvidia cuda-nvcc
10. from apex: pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --global-option="--cpp_ext" --global-option="--cuda_ext" ./
11. conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
12. mamba install conda-forge::nvidia-apex
13. mamba install torch


----------------
14. If you want to use the pre-made jsonlines documents, skip to step ___. Otherwise, create a folder in ASP/data called faa_conll

15. Edit ASP/configs/coref.conf lines 3-8 to look like this:

   dataset = "faa_conll"

   data_dir = \$\{ASP\}/data/faa_conll/ 
   
   model\_dir = \$\{ASP\}/data/faa_conll/ 
   
   log\_root = \$\{ASP\}/data/faa_conll/

11. Run each cell in the formatt_conll.ipynb notebook. This will put the FAA data into CONLL-12 format, using a '-' as a placeholder for most of the columns, since they are not used by ASP

12. From the ASP folder, run python ./data/t5minimize_coref.py ./data/faa_conll/ ./data/faa_conll/. Note that it has created jsonlines documents in the faa_conll folder.

13. If you have just ignored steps 4-7,

14. Change "ontonotes_coref" to "faa_conll" on line 38 and 80 in util/tensorize_coref.py

16. python evaluate_coref.py flant5_base tliu/asp-coref-flan-t5-base <GPU_ID>



 Package            Version  Build               Channel                    Size
───────────────────────────────────────────────────────────────────────────────────
  Install:
───────────────────────────────────────────────────────────────────────────────────

  + cffi              1.16.0  py38h5eee18b_0      pkgs/main/linux-64        258kB
  + cxxfilt            0.3.0  py38h17151c0_5      conda-forge/linux-64     Cached
  + exceptiongroup     1.0.4  py38h06a4308_0      pkgs/main/linux-64       Cached
  + iniconfig          1.1.1  pyhd3eb1b0_0        pkgs/main/noarch         Cached
  + mkl-service        2.4.0  py38h5eee18b_1      pkgs/main/linux-64         55kB
  + ninja             1.10.2  h06a4308_5          pkgs/main/linux-64       Cached
  + ninja-base        1.10.2  hd09550d_5          pkgs/main/linux-64       Cached
  + nvidia-apex        22.03  cpu_py38h31d9214_3  conda-forge/linux-64     Cached
  + pluggy             1.0.0  py38h06a4308_1      pkgs/main/linux-64       Cached
  + pycparser           2.21  pyhd3eb1b0_0        pkgs/main/noarch         Cached
  + pytest             7.4.0  py38h06a4308_0      pkgs/main/linux-64       Cached
  + tbb             2021.8.0  hdb19cb5_0          pkgs/main/linux-64       Cached
  + tomli              2.0.1  py38h06a4308_0      pkgs/main/linux-64       Cached

  Change:
───────────────────────────────────────────────────────────────────────────────────

  - libblas            3.9.0  16_linux64_mkl      conda-forge                    
  + libblas            3.9.0  1_h86c2bf4_netlib   conda-forge/linux-64      203kB
  - libcblas           3.9.0  16_linux64_mkl      conda-forge                    
  + libcblas           3.9.0  5_h92ddd45_netlib   conda-forge/linux-64       56kB
  - liblapack          3.9.0  16_linux64_mkl      conda-forge                    
  + liblapack          3.9.0  5_h92ddd45_netlib   conda-forge/linux-64        3MB

  Upgrade:
───────────────────────────────────────────────────────────────────────────────────

  - intel-openmp    2022.1.0  h9e868ea_3769       pkgs/main                      
  + intel-openmp    2023.1.0  hdb19cb5_46306      pkgs/main/linux-64       Cached
  - mkl             2022.1.0  hc2b9512_224        pkgs/main                      
  + mkl             2023.1.0  h213fc3f_46344      pkgs/main/linux-64       Cached

  Downgrade:
───────────────────────────────────────────────────────────────────────────────────

  - libprotobuf       4.24.4  hf27288f_0          conda-forge                    
  + libprotobuf       3.20.3  he621ea3_0          pkgs/main/linux-64       Cached
  - protobuf          4.24.4  py38hf14ab21_0      conda-forge                    
  + protobuf          3.20.3  py38h6a678d5_0      pkgs/main/linux-64        334kB
  - pytorch            2.1.2  py3.8_cpu_0         pytorch                        
  + pytorch            2.0.1  cpu_py38hdc00b08_0  pkgs/main/linux-64         69MB



Just now after pip install requirements.txt

Collecting truecase (from -r requirements.txt (line 1))
  Obtaining dependency information for truecase from https://files.pythonhosted.org/packages/6a/ec/ca9dc9ab492aebc57af351709355d74d90e2b71c2b75befd2a1bf2c5db78/truecase-0.0.14-py3-none-any.whl.metadata
  Downloading truecase-0.0.14-py3-none-any.whl.metadata (2.3 kB)
Collecting tqdm (from -r requirements.txt (line 2))
  Obtaining dependency information for tqdm from https://files.pythonhosted.org/packages/2a/14/e75e52d521442e2fcc9f1df3c5e456aead034203d4797867980de558ab34/tqdm-4.66.2-py3-none-any.whl.metadata
  Using cached tqdm-4.66.2-py3-none-any.whl.metadata (57 kB)
Collecting pyhocon (from -r requirements.txt (line 3))
  Using cached pyhocon-0.3.60.tar.gz (158 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting scipy (from -r requirements.txt (line 4))
  Obtaining dependency information for scipy from https://files.pythonhosted.org/packages/e8/fb/e5955e2ddbdf2baee461eb53ec8d0adedd20a6dfc5510ef8d5e7e44ba461/scipy-1.13.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
  Downloading scipy-1.13.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (60 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.6/60.6 kB 3.5 MB/s eta 0:00:00
Collecting numpy (from -r requirements.txt (line 5))
  Obtaining dependency information for numpy from https://files.pythonhosted.org/packages/3a/d0/edc009c27b406c4f9cbc79274d6e46d634d139075492ad055e3d68445925/numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
  Using cached numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
ERROR: Ignored the following versions that require a different python version: 1.21.2 Requires-Python >=3.7,<3.11; 1.21.3 Requires-Python >=3.7,<3.11; 1.21.4 Requires-Python >=3.7,<3.11; 1.21.5 Requires-Python >=3.7,<3.11; 1.21.6 Requires-Python >=3.7,<3.11; 1.6.2 Requires-Python >=3.7,<3.10; 1.6.3 Requires-Python >=3.7,<3.10; 1.7.0 Requires-Python >=3.7,<3.10; 1.7.1 Requires-Python >=3.7,<3.10; 1.7.2 Requires-Python >=3.7,<3.11; 1.7.3 Requires-Python >=3.7,<3.11; 1.8.0 Requires-Python >=3.8,<3.11; 1.8.0rc1 Requires-Python >=3.8,<3.11; 1.8.0rc2 Requires-Python >=3.8,<3.11; 1.8.0rc3 Requires-Python >=3.8,<3.11; 1.8.0rc4 Requires-Python >=3.8,<3.11; 1.8.1 Requires-Python >=3.8,<3.11
ERROR: Could not find a version that satisfies the requirement python==3.8 (from versions: none)
ERROR: No matching distribution found for python==3.8

pip install numpy pyhocon torch transformers