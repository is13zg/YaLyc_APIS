import maps
import sys


def main():
    toponym_to_find = " ".join(sys.argv[1:])

    add_params = {
        "ll": maps.get_coords(toponym_to_find),
        "spn": maps.get_span(toponym_to_find),
        "text": "аптека"
    }

    # Получаем координаты ближайшей аптеки.
    org = maps.get_org(add_params)
    org_ll = org["geometry"]["coordinates"]
    add_params.pop("text")
    add_params["pt"] = f"{org_ll[0]},{org_ll[1]}"
    #maps.show_map(add_params)

    add_params["pt"] += "~" + add_params["ll"]
    maps.show_map(add_params)

    add_params['map'] = "l"
    add_params.pop("spn")
    maps.show_map(add_params)

    # Сниппет
    # Название организации.
    name = org["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    address = org["properties"]["CompanyMetaData"]["address"]
    # Время работы
    time = org["properties"]["CompanyMetaData"]["Hours"]["text"]
    # Расстояние

    distance = round(
        maps.lonlat_distance((float(add_params["ll"].split(",")[0]), float(add_params["ll"].split(",")[1])),
                             (org_ll[0], org_ll[1])))
    snippet = f"Название:\t{name}\nАдрес:\t{address}\nВремя работы:\t{time}\nРасстояние:\t{distance}м."
    print(snippet)


if __name__ == "__main__":
    main()
