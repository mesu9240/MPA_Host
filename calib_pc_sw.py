#sw for calibration to dsPIC30F4011

#import modules
import serial
import os
import time
# definition of utlity functions
# function hex_str_2_char convers a two digits hex number into its according ASCII char
def hex_str_2_char(hex_str): # TODO: think about fault tolerance
	return chr(int(hex_str, 16))

# function converts a ascii char into hex string without 0x
def char_2_hex_str(ascii_char):
	hex_str = hex(ord(ascii_char))
	return hex_str[2:] # remove 0x

#create serial object associated with COM3 (USB RS232 adapter)
ser = serial.Serial('COM3')
os.system('cls')
os.system('color F') # text light green
print "...starting calibration software...\r\n"
print "...trying to open port COM3...\r\n"
if ser.isOpen():
	# start calibration operation if COM3 is open
	# process calibration commands and initiate operations
	print "\n   Available calibration commands:\r\n"
	print   "   1: Read data memory\r\n"
	print   "   2: Write data memory\r\n"
	print   "   q: Canel action\r\n"
	cmd_str = raw_input("   Input your command option:>> ")
	while cmd_str != 'q':
		if cmd_str == "1": #read data memory
			print "\r\n"
			addr_str = raw_input("Address of memory (0xNNNN) to be read: >>") # input RAM address
			print "\r\n"
			mcu_fdb_byte = 'F';
			ser.write('c')
			print "wrting command character c \r\n"
			ser.write('a')
			print "wrting command character a \r\n"
			ser.write(chr(int(addr_str[2:4],16)))
			print "wrting upper byte of the address\r\n"
			ser.write(chr(int(addr_str[4:],16)))
			print "wrting lower byte of the address\r\n"			
			for timeout_cnt in range(5):# mcu takes time to respond to calibration commands
				timeout_cnt = timeout_cnt + 1
				time.sleep(1)
				if ser.in_waiting == 1:
					mcu_fdb_byte = ser.read(1)
					print "mcu returning message " + mcu_fdb_byte + "\r\n"
					print "calibration read action failed\r\n"
					break
				elif ser.in_waiting == 4:
					mcu_fdb_byte = ser.read(4)
					upperbyte = hex(ord(mcu_fdb_byte[1]))
					lowerbyte = hex(ord(mcu_fdb_byte[0]))
					print "The contend of address " + addr_str + " is : "
					print upperbyte + lowerbyte[2:] + mcu_fdb_byte[2:]
					break
			if timeout_cnt is 5L:# 5s is considered time out		
				print "read action time out, mcu is not responding \r\n"			
		elif cmd_str == "2": #write data memory
			print "\r\n"
			addr_str = raw_input("Address (0xNNNN) to be written: >>")
			print "\r\n"
			ser.write('c')
			ser.write('b')
			ser.write(hex_str_2_char(addr_str[2:4]))
			ser.write(hex_str_2_char(addr_str[4:]))
			for timeout_cnt in range(5):
				time.sleep(1)
				if ser.in_waiting == 2:
					mcu_fdb_addr = ser.read(2)
					print "Address to be written: 0x" + char_2_hex_str(mcu_fdb_addr[0]) \
													  + char_2_hex_str(mcu_fdb_addr[1])
					# start writing memory
					print "\r\n"
					calib_wrt_data = raw_input("Input data to write: >>")
					ser.write('c')
					ser.write('c')
					ser.write(hex_str_2_char(calib_wrt_data[2:4]))
					ser.write(hex_str_2_char(calib_wrt_data[4:]))
					break
			if timeout_cnt is 5L:
				print "write action is not acknowledged by mcu\r\n"
			
		else: # invalid commands
			print "invalid command\r\n"
		cmd_str = raw_input("   Next command option:>>")
	print "\nLeaving SW, closing serial port COM3..."	
	ser.close()
else:
	# port is not open, alert user and close port
	ser.close()
	print "Something is wrong with COM3 port, calibration aborted.\r\n"
os.system('cls')
os.system('color A') # turn command line back to light green