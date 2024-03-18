To get picam running you have to install libcap dev headers:

```sudo apt-get install build-essential libcap-dev```

and

```sudo apt install -y python3-libcamera```

Also if you want to use picam in a venv you have to create the venv with ```--system-site-package``` f.e.

```python -m venv .venv --system-site-packages```