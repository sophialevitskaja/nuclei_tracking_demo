import numpy as np
import fsspec, zarr
from matplotlib.colors import LinearSegmentedColormap
from skimage import filters, feature, segmentation, morphology

PINK, PLUM = "#d63384", "#7a1d6b"

pink_fluor = LinearSegmentedColormap.from_list(
    "pink_fluor",
    ["#000000", "#2a0b2e", "#7a1d6b", "#d63384", "#ff8fc0", "#fff0f6"],
)

URL = "https://public.czbiohub.org/royerlab/zebrahub/imaging/single-objective/ZSNS001_tail.ome.zarr"


def open_level(level, url=URL):
    return zarr.open_array(fsspec.get_mapper(f"{url}/{level}"), mode="r")


def segment_frame(f, inside, s_small=0.7, s_mask=1.5, s_large=6.0, seed_thr=0.03,
                   min_dist=2, block=21, offset=0.0, floor=0.10, min_size=6):
    sm = filters.gaussian(f, s_small)          # for seeds
    sm_mask = filters.gaussian(f, s_mask)      # for outlines

    dog = sm - filters.gaussian(f, s_large)
    seeds = feature.peak_local_max(dog, min_distance=min_dist,
                                   threshold_abs=seed_thr,
                                   labels=inside.astype(int))
    markers = np.zeros(f.shape, dtype=int)
    markers[tuple(seeds.T)] = np.arange(1, len(seeds) + 1)

    fg = sm_mask > filters.threshold_local(sm_mask, block_size=block, offset=offset)
    fg &= inside & (sm_mask > floor)
    fg = morphology.remove_small_objects(fg, max_size=min_size - 1)

    labels = segmentation.watershed(-sm_mask, markers, mask=fg)
    return labels, seeds