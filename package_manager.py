

try:
    import pip
except ImportError:
    # installing pip
    if 'n' in input("pip is not installed, press 'n' to quit."):
        exit()

    pipUrl = "https://bootstrap.pypa.io/get-pip.py"
    
    from urllib.request import urlopen
    import tempfile 

    with urlopen(pipUrl) as response:
        getpip_py = response.read()
        eval(getpip_py)
        import pip


def install_selenium():
    pass
    