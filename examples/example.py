from libfledge.nodes import NOAA, get_node_verbs, kind_name

if __name__ == "__main__":
    noaa = NOAA()
    print(get_node_verbs(noaa))
    print(get_node_verbs(noaa).to_dict())
