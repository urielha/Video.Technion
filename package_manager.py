def install_pip():
    try:
        import pip
        return None
    except ImportError:
        # installing pip
        if "y" != input(
                "pip is not installed, press 'y' to install: ").lower():
            input("Exiting - Press Enter to quit ")
            exit()

    pipUrl = "https://bootstrap.pypa.io/get-pip.py"

    from urllib.request import urlopen

    with open("get-pip.py", "wb") as getpip_py:
        with urlopen(pipUrl) as response:
            getpip_py.write(response.read())
    from os import system, remove
    from sys import executable as PythonExec
    system("{} {}".format(PythonExec, getpip_py.name))
    remove("get-pip.py")
    print("-" * 40)
    print("")


def install_req():
    import pip
    try:
        from selenium import webdriver
        return None
    except ImportError:
        if "y" != input(
                "selenium is not installed, press 'y' to install: ").lower():
            input("Exiting - Press Enter to quit ")
            exit()

    pip.main(['install', '-r', 'requirements.txt'])
    print("-" * 40)
    print("")
