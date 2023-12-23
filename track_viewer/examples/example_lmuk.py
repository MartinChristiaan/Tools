"""Experimental file testing functionality if everything is a Panel"""

from guitoolbox.app import MainGUI, SyncMode
from media_manager.core import MediaManager
from trackertoolbox.tracks import Tracks

if __name__ == "__main__":
    media_manager_0 = MediaManager(
        # filepath=r"C:\Users\rooijenalv\Downloads\20230309T114435\video\camera00",
        filepath=r"C:\Users\rooijenalv\Downloads\20230309T114435\video\camera01",
        video_suffix=".avi",
        log_column_to_use=1,
        # filepath=r"\\diskstationii1\lm_uk\data\20221219_data_from_LM\video\Main_Clip",
        # video_suffix=".mp4",
    )
    # media_manager_1 = MediaManager(
    #     filepath=r"\\diskstationii1\lm_uk\data\20221219_data_from_LM\video\Main_Clip",
    #     video_suffix=".mp4",
    # )
    tracks_0 = Tracks.load(
        # filename=r"C:\Users\rooijenalv\Downloads\20230309T114435\results\camera00\tracks_11.csv"
        filename=r"C:\Users\rooijenalv\Downloads\20230309T114435\results\camera01\tracks_11.csv"
        # filename=r"\\diskstationii1\lm_uk\data\20221219_data_from_LM\results\main_clip\main_clip\tracking_mmYes_resizeYes_conf10_NLM_L_1CLS_1280_size1560\tracks_fil_4reid.csv"
    )
    # tracks_1 = Tracks.load(
    #     filename=r"\\diskstationii1\lm_uk\data\20221219_data_from_LM\results\main_clip\main_clip\tracking_mmYes_resizeYes_conf10_NLM_L_1CLS_1280_size1560\tracks_fil_4reid.csv"
    # )

    gui = MainGUI(
        videos=[
            media_manager_0,
            # media_manager_1,
        ],
        tracks=[
            tracks_0,
            # tracks_1,
        ],
        sync_mode=SyncMode.ALL,
    )
