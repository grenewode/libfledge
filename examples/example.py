from libfledge.nodes import NOAA, kind_name

if __name__ == "__main__":
    noaa = NOAA()
    print(noaa.__class__.__name__)
    print(kind_name(noaa))
