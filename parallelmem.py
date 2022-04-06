from utime import sleep, sleep_ms, sleep_us
from machine import Pin

class ParallelMem:
    # GPIO 3, 4, and 5 are free for use
    def __init__(self):
        # RAM Control Out lines
        self.current_addr = 0x0
        self.timings = 0
        self.write_enable = Pin(0, Pin.OUT, Pin.PULL_UP)
        self.output_enable = Pin(1, Pin.OUT, Pin.PULL_UP)
        self.chip_enable = Pin(2, Pin.OUT, Pin.PULL_UP)
        
        # Setup bus lines
        self.write_enable.value(1) # ACTIVE LOW, Set HIGH
        self.output_enable.value(1) # ACTIVE LOW, Set HIGH
        self.chip_enable.value(1) # ACTIVE LOW, Set HIGH
        
        self.max_mem = (2**12)-1
        # 11-Bit Address Out Lines (2048 bytes of memory)
        self.addr_0 = Pin(17, Pin.OUT)
        self.addr_1 = Pin(16, Pin.OUT)
        self.addr_2 = Pin(15, Pin.OUT)
        self.addr_3 = Pin(14, Pin.OUT)
        self.addr_4 = Pin(13, Pin.OUT)
        self.addr_5 = Pin(12, Pin.OUT)
        self.addr_6 = Pin(11, Pin.OUT)
        self.addr_7 = Pin(10, Pin.OUT)
        self.addr_8 = Pin(9, Pin.OUT)
        self.addr_9 = Pin(8, Pin.OUT)
        self.addr_10 = Pin(7, Pin.OUT)
        self.addr_11 = Pin(6, Pin.OUT)
        #print("Specifying {0} as maximum memory address".format(str(hex(self.max_mem))))

        # 8-Bit Data Lines
        self.data_0 = Pin(28, Pin.IN)
        self.data_1 = Pin(27, Pin.IN)
        self.data_2 = Pin(26, Pin.IN)
        self.data_3 = Pin(22, Pin.IN)
        self.data_4 = Pin(21, Pin.IN)
        self.data_5 = Pin(20, Pin.IN)
        self.data_6 = Pin(19, Pin.IN)
        self.data_7 = Pin(18, Pin.IN)
    
    def idle_mode(self):
        self.write_enable.value(1) # ACTIVE LOW, Set HIGH
        self.output_enable.value(1) # ACTIVE LOW, Set HIGH
        self.chip_enable.value(1) # ACTIVE LOW, Set HIGH
        sleep_us(self.timings)
    
    def write_mode(self):
        self.write_enable.value(0) # ACTIVE LOW, Set LOW
        self.output_enable.value(1) # ACTIVE LOW, Set HIGH
        self.chip_enable.value(0) # ACTIVE LOW, Set LOW
        sleep_us(self.timings)
    
    def read_mode(self):
        self.write_enable.value(1) # ACTIVE LOW, Set HIGH
        self.output_enable.value(0) # ACTIVE LOW, Set LOW
        self.chip_enable.value(0) # ACTIVE LOW, Set LOW
        sleep_us(self.timings)
    
    def address(self, addr):
        tmp_data = bin(int(addr))
        
        # Fill in missing bits
        tmp_payload = str(tmp_data).replace('0b', '')
        for missing in range(0, (12-len(tmp_payload))):
            tmp_payload = ("0" + tmp_payload)
        payload = []
        
        # Convert string to ints
        for convert in tmp_payload:
            if convert == "0":
                payload.append(0)
            else:
                payload.append(1)
        
        #print("addr: {0}".format(payload))
        
        # Write address to bus
        self.addr_0.value(payload[0])
        self.addr_1.value(payload[1])
        self.addr_2.value(payload[2])
        self.addr_3.value(payload[3])
        self.addr_4.value(payload[4])
        self.addr_5.value(payload[5])
        self.addr_6.value(payload[6])
        self.addr_7.value(payload[7])
        self.addr_8.value(payload[8])
        self.addr_9.value(payload[9])
        self.addr_10.value(payload[10])
        self.addr_11.value(payload[11])
        sleep_us(self.timings)
        self.current_addr = addr
        #return payload
    
    def write(self, data):
        # Reconfigure data pins to be in write mode
        self.data_0.init(self.data_0.OUT)
        self.data_1.init(self.data_1.OUT)
        self.data_2.init(self.data_2.OUT)
        self.data_3.init(self.data_3.OUT)
        self.data_4.init(self.data_4.OUT)
        self.data_5.init(self.data_5.OUT)
        self.data_6.init(self.data_6.OUT)
        self.data_7.init(self.data_7.OUT)
        
        # Write data
        if type(data) == int:
            tmp_data = bin(data)
        elif type(data) == hex:
            tmp_data == bin(int(data))
        elif type(data) == bin:
            tmp_data = data
        else:
            print("Invalid type")
            return
        
        # Convert data into parallel binary format
        tmp_payload = str(tmp_data).replace('0b', '')
        for missing in range(0, (8-len(tmp_payload))):
            tmp_payload = ("0" + tmp_payload)
        payload = []
        for convert in tmp_payload:
            if convert == "0":
                payload.append(0)
            else:
                payload.append(1)
        
        #print("write: {0}".format(payload))
        
        # Write binary to data lines
        self.data_0.value(payload[0])
        self.data_1.value(payload[1])
        self.data_2.value(payload[2])
        self.data_3.value(payload[3])
        self.data_4.value(payload[4])
        self.data_5.value(payload[5])
        self.data_6.value(payload[6])
        self.data_7.value(payload[7])
        
        # Enable the chip and put in write mode
        self.write_mode()
        
        # Disable the chip
        self.idle_mode()
    
    def read(self):
        # Reconfigure pins to be in read mode
        self.data_0.init(self.data_0.IN, self.data_0.PULL_DOWN)
        self.data_1.init(self.data_1.IN, self.data_1.PULL_DOWN)
        self.data_2.init(self.data_2.IN, self.data_2.PULL_DOWN)
        self.data_3.init(self.data_3.IN, self.data_3.PULL_DOWN)
        self.data_4.init(self.data_4.IN, self.data_4.PULL_DOWN)
        self.data_5.init(self.data_5.IN, self.data_5.PULL_DOWN)
        self.data_6.init(self.data_6.IN, self.data_6.PULL_DOWN)
        self.data_7.init(self.data_7.IN, self.data_7.PULL_DOWN)
        
        # Enable the chip and put in read mode
        self.read_mode()
         
        # Read the data line states
        output = []
        output.append(self.data_0.value())
        output.append(self.data_1.value())
        output.append(self.data_2.value())
        output.append(self.data_3.value())
        output.append(self.data_4.value())
        output.append(self.data_5.value())
        output.append(self.data_6.value())
        output.append(self.data_7.value())
        
        # Disable the chip
        self.idle_mode()
        
        num = 0
        for bit in output:
            num = 2 * num + bit
        return num

    def test(self):
        bad_addr = 0
        bad_addrs = []
        for addr in range(0x00, self.max_mem):
            self.address(addr)
            for sample in [0b10101010, 0b01010101, 0b11111111, 0b00000000]:
                self.write(sample)
                data_back = self.read()
                if not data_back == sample:
                    #print("Found bad address at {0} during {1} test".format(hex(addr), str(bin(sample))))
                    if not addr in bad_addrs:
                        bad_addr += 1
                        bad_addrs.append(addr)
        print("100%!")
        return bad_addr, bad_addrs
    
    def clear(self):
        for addr in range(0x00, self.max_mem):
            self.address(addr)
            self.write(0x00)
    
    def bulk_write(self, data):
        bad_writes = []
        if len(data) > self.max_mem:
            print("Warning! There are not enough memory addresses to store this payload, so some bytes will not be written.")
        
        for i in range(0x00, len(data)):
            if (not((i+1) > self.max_mem)):
                self.address(i)
                self.write(data[i])
                readback = self.read()
                if not readback == data[i]:
                    if not i in bad_writes:
                        bad_writes.append(i)
                    print("Write error at {0} expecting {1} got {2}".format(hex(i), hex(data[i]), hex(readback)))
            else:
                if (i+1) > self.max_mem:
                    print("Maximum amount of memory space reached!")
                    break
        return bad_writes
        
    def verify(self, data):
        bad_reads = []
        if len(data) > self.max_mem:
            print("Warning! The verification payload is larger than the amount of available memory addresses, so some bytes will not be verified.")
        
        for i in range(0x00, len(data)):
            if (not((i+1) > self.max_mem)):
                self.address(i)
                readback = self.read()
                if not readback == data[i]:
                    if not i in bad_reads:
                        bad_reads.append(i)
                    print("Verify error at {0} expecting {1} got {2}".format(hex(i), hex(data[i]), hex(readback)))
            else:
                if (i+1) > self.max_mem:
                    print("Maximum amount of memory space reached!")
                    break
        return bad_reads

    def bulk_read(self):
        readback = []
        for i in range(0x00, self.max_mem):
            self.address(i)
            readback.append(self.read())
        return readback
