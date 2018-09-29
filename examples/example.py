from libfledge.nodes.weather import NOAA

if __name__ == "__main__":
    noaa = NOAA()
    print(noaa.node_verbs())
