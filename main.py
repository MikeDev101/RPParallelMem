from parallelmem import ParallelMem

if __name__ == "__main__":
    ram = ParallelMem() # Defaults to 8-bit words, 11-bit addresses. Only GPIO 3, 4, and 5 are available.
    
     """
    Control line wiring
    GPIO Pin       Memory Pin
    0              Write Enable
    1              Output Enable
    2              Chip Enable

    Address bus wiring
    17             A0
    16             A1
    15             A2
    14             A2
    13             A4
    12             A5
    11             A6
    10             A7
    9              A8
    8              A9
    7              A10
    6              A11
    
    Data bus wiring
    28             D0
    27             D1
    26             D2
    22             D3
    21             D4
    20             D5
    19             D6
    18             D7
    """
    
    # Tests
    print("The maximum amount of RAM available is {0} words.".format(ram.max_mem)) # Depending upon your configuration in parallelmem.py, this will return the largest memory size in bytes. (addresses * word size)
    
    print("Clearing RAM...")
    ram.clear() # Fills all available memory addresses with 0x00, or a bunch of zeros.
    
    print("Testing RAM, please wait...")
    print(ram.test()) # Runs a thorough RAM test. Returns a tuple containing the number of bad addresses, and a list containing all bad addresses.
    
    print("Going to 0xfff")
    ram.address(0xfff) # Goto 0xfff.
    print("Reading 0xfff")
    print(ram.read()) # Reads the selected address.
    print("Writing 0xff to 0xfff")
    ram.write(0xff) # Writes a value to that address.
    print("Reading 0x000")
    print(ram.read()) # Reads the selected address.
    print("Bulk writing data")
    print(ram.bulk_write([0xff, 0x25, 25, 0b11111111])) # Copys a list. Supports copying intergers, hex, and binary. Must not be larger than maximum word length (default: 8-bits, 0xff, or 255.) Returns a list of bad addresses.
    print("Reading all of RAM")
    print(ram.bulk_read()) # Returns the entire RAM contents as a list.
    print("Verifying bulk data...")
    print(ram.verify([0xff, 0x25, 25, 0b11111111])) # Returns a list of bad addresses. If data is valid, will return with an empty list.
