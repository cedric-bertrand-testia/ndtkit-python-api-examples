from ndtkit_api import NDTKitAScanInterface

""" Parameters """
input_ascan_path = "path/to/ascan"


if __name__ == "__main__":
    # Open the A-Scan file
    ascan_frame = NDTKitAScanInterface.open_ascan(input_ascan_path, 0)

    # Get the number of rows in the A-Scan frame
    row_count = ascan_frame.get_row_number()

    # Find the maximum amplitude value in the A-Scan data
    max_value = float('-inf')
    for row in range(row_count):
        ascans_row = ascan_frame.get_row(row)
        for ascan in ascans_row:
            data = ascan.get_amp_values()
            max_value = max(max_value, max(data))
    print(f"Maximum amplitude value in the A-Scan data: {max_value}")

