from ndtkit_api import NDTKitAScanInterface

""" Parameters """
input_ascan_path = "path/to/ascan"


if __name__ == "__main__":
    # Open the A-Scan file
    ascan_frame = NDTKitAScanInterface.open_ascan(input_ascan_path, 0)

    # Get the number of rows in the A-Scan frame
    row_count = ascan_frame.get_row_count()

    # Get all amplitude values for the entire A-Scan frame
    tof_amp_values = ascan_frame.get_row_tof_amp(0, row_count)

    # Calculate the maximum amplitude value across all A-Scans in the frame
    max_val = max((max(ascan[1]) for line in tof_amp_values for ascan in line if len(ascan[1]) > 0), default=0)

    # Find the maximum amplitude value in the A-Scan data
    print(f"Maximum amplitude value in the A-Scan data: {max_val}")
