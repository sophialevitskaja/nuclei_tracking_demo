def open_level(level, url=URL):
    return zarr.open_array(fsspec.get_mapper(f"{url}/{level}"), mode="r")

pink_fluor = LinearSegmentedColormap.from_list(
    "pink_fluor",
    ["#000000", "#2a0b2e", "#7a1d6b", "#d63384", "#ff8fc0", "#fff0f6"],
)