"""Experimental file testing functionality if everything is a Panel"""

from guitoolbox.app import MainGUI, SyncMode
from media_manager.core import MediaManager

if __name__ == "__main__":
    media_manager_0 = MediaManager(
        filepath=r"\\diskstationii1\scanvision\data\kmar_cna_reorganized\video\camera01",
        video_suffix=".mp4",
    )
    media_manager_1 = MediaManager(
        filepath=r"\\diskstationii1\scanvision\data\kmar_cna_reorganized\video\camera02",
        video_suffix=".mp4",
    )
    # TODO implement
    # tracks_0 = MediaManagerTrackLoader(
    #     video_dirpath=r"\\diskstationii1\scanvision\data\kmar_cna_reorganized\video\camera01",
    #     video_suffix=".mp4",
    #     result_dirpath=r"\\diskstationii1\scanvision\data\kmar_cna_reorganized\results\camera01",
    #     tracks_filename="tracker_v3.csv",
    # )
    # TODO implement
    # tracks_1 = MediaManagerTrackLoader(
    #     video_dirpath=r"\\diskstationii1\scanvision\data\kmar_cna_reorganized\video\camera02",
    #     video_suffix=".mp4",
    #     result_dirpath=r"\\diskstationii1\scanvision\data\kmar_cna_reorganized\results\camera02",
    #     tracks_filename="tracker_v3.csv",
    # )

    gui = MainGUI(
        videos=[media_manager_0, media_manager_1],
        # tracks=[tracks_0, tracks_1],
        sync_mode=SyncMode.VIDEO,
    )

    # TODO
    # in_background = False  # Or set in_background=False wait here until the program is closed by the user
    # if in_background:
    #     thread = Thread(target=gui.run)
    #     thread.start()
    # else:
    #     gui.run()
    #     thread = None
    #
    # # TODO update tracks
    #
    # # TODO interface could be made simpler
    # # Adjust the plot as you like here
    # # import pdb; pdb.set_trace()  # Some time needs to pass before below lines can be executed, putting a break point here
    # widget = gui.panels_gui._panels[1].track_plot_widget
    # axes = widget.axes
    # figure = axes.get_figure()
    # axes.plot([0, 7000], [0, 2000], c="r")
    # widget.tracks
    # widget.render()
    #
    # if thread is not None:
    #     thread.join()  # Useful if app runs in the background, code waits here untils the user closes the program
