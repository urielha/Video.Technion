
def install_pip():
    try:
        import pip
    except ImportError:
        # installing pip
        if 'y' != input("pip is not installed, press 'y' to install: ").lower():
            input("Exiting - Press Enter to quit ")
            exit()

        pipUrl = "https://bootstrap.pypa.io/get-pip.py"

        from urllib.request import urlopen

        with urlopen(pipUrl) as response:
            getpip_py = response.read()
            eval(getpip_py)
            import pip


def install_req():
    import pip
    pip.main(['install', '-q', '-r', 'requirements.txt'])
    