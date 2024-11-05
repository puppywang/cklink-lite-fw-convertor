#!/usr/bin/env python

import os
import sys


# Main script function
def main():
    # If no argument, show usage
    if len(sys.argv) != 2:
        print("Convert CK-Link Lite firmware for stm32f103")
        print("")
        print("Usage: python cklink_lite_fw_converter.py cklink_lite.hex")
        print("")
        print("'cklink_lite.hex' can be found in C-Sky debug server.")
        sys.exit(1)

    cklink_file_name = sys.argv[1]

    # Generate final result filename
    result_file_name = os.path.splitext(os.path.basename(cklink_file_name))[0] + "_for-stm32f103.hex"

    # Find first line with address 0x41XX
    realloc_lines = []
    
    with open(cklink_file_name, 'r') as f:
        for i, line in enumerate(f, start=1):
            if line.startswith(":1041"):
                f_line = i
                break
            elif line.startswith(":1040"):
                line = line.replace(":1040", ":1000").rstrip('\n')
                line_data = [int(line[x:x+2], 16) for x in range(1, len(line), 2)]
                chksum = ((sum(line_data[:-1]) ^ 0xff) + 1) & 0xff
                realloc_lines.append(line.rstrip()[:-2] + str(hex(chksum)[2:]).upper() + "\n")
            else:
                realloc_lines.append(line)
    
    if f_line is None:
        print("Error: No line found with address 0x41XX.")
        sys.exit(1)

    # Remove result file if it exists
    if os.path.exists(result_file_name):
        os.remove(result_file_name)

    # Merge converted and original file together
    with open(result_file_name, 'w') as result:
        result.writelines(realloc_lines)
        with open(cklink_file_name, 'r') as original:
            result.write(original.read())

    print(f"'{cklink_file_name}' converted and saved as '{result_file_name}'")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
