import dlutils_ii as du


def get_mantis():
    pf = du.Pathfinder(
        "mantis_drone_2023",
        "DJI_202309100220_001/wide_hd",
        basedir=r"\\wsl.localhost\Ubuntu\diskstation",
        cache_dir=r"c:/Data/dataset",
    )

    o = du.TrainOptions(
        False,
        [1],
        max_samples=300,
        motion_models="motion_models.csv",
        annotations_suffix=None,
    )
    return du.DatasetConfig(pf, o)


def get_marnehuizen():
    pf = du.Pathfinder(
        "marnehuizen_2013",
        "",
        basedir=None,
        cache_dir="./dataset",
    )

    o = du.TrainOptions(
        False,
        [1],
        max_samples=300,
        motion_models="motion_models.csv",
        annotations_suffix=None,
    )
    return du.DatasetConfig(pf, o)
