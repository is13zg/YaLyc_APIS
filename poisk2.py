import maps
import sys
from PIL import Image
from io import BytesIO
import requests


def main():
    name = " ".join(sys.argv[1:])

    if name:

        maps.show_map(
            {"ll": maps.get_coords(name),
             "spn": maps.get_span(name),
             "pt": maps.get_coords(name)}
        )
    else:
        print('No data')


if __name__ == "__main__":
    main()
