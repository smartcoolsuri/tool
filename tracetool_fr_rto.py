import os #for sys command
import sys #for input
import getopt #for input handling
import logging
import time
import types
import string

# Align center is not supported because of the terrible form :)
ALIGN_RIGHT   = 0x0001
ALIGN_LEFT    = 0x0002
PADDING_LEFT  = 0x0010
PADDING_RIGHT = 0x0020
PADDING_ALL   = PADDING_LEFT | PADDING_RIGHT

def _rpad_to_maxlen(slist, padchar=' '):
    maxlen = max(map(len, slist))
    res = map(lambda s: s + padchar * (maxlen - len(s)), slist)
    return res

def _lpad_to_maxlen(slist, padchar=' '):
    maxlen = max(map(len, slist))
    res = map(lambda s: padchar * (maxlen - len(s)) + s, slist)
    return res

def test_mask(mask, flag):
    '''
    tests mask for all bits of flag set
    '''
    return mask & flag == flag

def _align_para(para, mode):
    if test_mask(mode, ALIGN_RIGHT):
        para = _lpad_to_maxlen(para) # little confusing: right align == left padding
    elif test_mask(mode, ALIGN_LEFT):
        para = _rpad_to_maxlen(para)
    else:
        raise ValueError, "NO ALIGN SPECIFIED!"

    if test_mask(mode, PADDING_LEFT):
        para = map(lambda x: ' ' + x, para)
    if test_mask(mode, PADDING_RIGHT):
        para = map(lambda x: x + ' ', para)

    return para

def _glue_cols(col1, col2):
    return map(lambda x: '%s|%s' % (x[0], x[1]), zip(col1, col2))

def _has_column_headers(cols):
    fail_count = 0
    for c in cols:
        try:
            a = c[2]
        except IndexError:
            fail_count += 1
    return fail_count == 0

def _join_to_list(*arguments):
    '''
    join all parameters to one list, 
    expanding lists and tuples
    '''
    res = list()
    for arg in arguments:
        if isinstance(arg, types.ListType):
            res.extend(arg)
        elif isinstance(arg, types.TupleType):
            res.extend(list(arg))
        else:
            res.append(arg)
    return res

def format_table(cols):
    # 1. aligning data
    if len(cols) == 0:
        return list()

    header_present = _has_column_headers(cols)
    if header_present:
        # prefix all data with headers // TODO: alignment set to center 
        cols = map(lambda x: [_join_to_list(x[2], x[0]), x[1] ], cols)

    cols2 = map(lambda x: _align_para(x[0], x[1]), cols)
    if len(cols2) == 0:
        return list()

    empty_vert_border = [ '' ] * len(cols2[0])

    cols2.append(empty_vert_border)
    cols2.insert(0, empty_vert_border)

    glued_cols = reduce(_glue_cols, cols2)
    if len(glued_cols) == 0:
        return list()

    border = '=' * len(glued_cols[0])
    glued_cols.insert(0, border)
    glued_cols.append(border)
    if header_present:
        glued_cols.insert(2, border)  # insert delimiter berween header and values        

    return glued_cols









Stream_list = []

class Packet:
	def __init__(self):
		self.frame_number = None		
		self.rx_num = None
		self.flags = None
		self.checksum = None
		self.expert_msg = None
		self.pcb_no = None	
		self.lpcb_no = None
		self.timestamp = None
		self.seq_num = None
		self.ack_num = None
		self.tcp_len = None
		self.win_size_cal = None
		self.win_size = None
		self.win_scale = None
		self.dup_ack = None
		self.dup_ack_num = None
		self.next_seq = None
		self.frame_time = None
			
		
class Stream:
	def __init__(self):
		self.stream_num = None 
		self.source_ip = None
		self.destination_ip = None
		self.source_port = None
		self.destination_port = None
		self.ws_val_cl = None
		self.mss_val_cl = None
		self.ws_val_svr = None
		self.ws_en = None		
		self.packets = []			

streams = []

class ack_fre:
	def __init__(self):
		self.seq = None
		self.ack = None
		self.freq = None
		self.time = None

ack_frequency = []


	
	
def filter_stream(filters, print_option):
	filter_list = filters.split()
	print filter_list
	if filter_list[0] == "ip.addr" :
		for s in streams :
			if s.source_ip == filter_list[2] or s.destination_ip == filter_list[2]:
				print_data(s.stream_num,print_option)
	elif filter_list[0] == "ip.src" :
		for s in streams :
			if s.source_ip == filter_list[2] :
				print_data(s.stream_num,print_option)
	elif filter_list[0] == "ip.dst" :
		for s in streams :
			if s.destination_ip == filter_list[2] :
				print_data(s.stream_num,print_option)
	elif filter_list[0] == "tcp.srcport" :
		for s in streams :
			if s.source_port == filter_list[2] :
				print_data(s.stream_num,print_option)
	elif filter_list[0] == "tcp.dstport" :
		for s in streams :
			if s.destination_port == filter_list[2] :
				print_data(s.stream_num,print_option)
	else :
		print "!!!!does not exists!!!!!"
	

	
def print_data(stream_number_selected,print_option):
		stream_number_filtered = str(stream_number_selected)		
		stream_number_print = []
		source_ip_print = []
		source_port_print = []
		destination_ip_print = []
		destination_port_print = []		
		frame_number_print = []		
		time_print = []
		flags_print = []
		seq_print = []
		ack_print = []
		tcp_len_print = []
		win_size_print = []
		win_scale_print = []
		dup_ack_num_print = []
		next_seq_print = []
		msg_print = []	
		direction_print = []		
		st_no_print = []
		number = 1		
		counter = 0
		lines_stream = ''	
		all_pack = 0
		#print print_option
		for s in streams :
			if  stream_number_selected == counter:							
				stream_number_print.append(s.stream_num)
				source_ip_print.append(s.source_ip)
				source_port_print.append(s.source_port)
				destination_ip_print.append(s.destination_ip)
				destination_port_print.append(s.destination_port)
				lines_stream = format_table( [(stream_number_print, ALIGN_RIGHT|PADDING_ALL, 'Stream Num'),(source_ip_print, ALIGN_RIGHT|PADDING_ALL, 'Src IP'), (source_port_print, ALIGN_RIGHT|PADDING_ALL, 'Src Port'),(destination_ip_print, ALIGN_RIGHT|PADDING_ALL, 'Dst IP'),(destination_port_print, ALIGN_RIGHT|PADDING_ALL, 'Dst Port')])
			elif not stream_number_filtered.isdigit():			
				stream_number_print.append(s.stream_num)
				source_ip_print.append(s.source_ip)
				source_port_print.append(s.source_port)
				destination_ip_print.append(s.destination_ip)
				destination_port_print.append(s.destination_port)
				lines_stream = format_table( [(stream_number_print, ALIGN_RIGHT|PADDING_ALL, 'Stream Num'),(source_ip_print, ALIGN_RIGHT|PADDING_ALL, 'Src IP'), (source_port_print, ALIGN_RIGHT|PADDING_ALL, 'Src Port'),(destination_ip_print, ALIGN_RIGHT|PADDING_ALL, 'Dst IP'),(destination_port_print, ALIGN_RIGHT|PADDING_ALL, 'Dst Port')])
			#print print_option + number	
			all_pack = 0
			counter = counter + 1
			if str(print_option) == str(number):
				if all_pack == 0 :
					if  stream_number_selected == (counter-1) or not stream_number_filtered.isdigit():
						print '\n'.join(lines_stream)
					lines_stream = ''
					stream_number_print[:] = []
					source_ip_print[:] = []
					source_port_print[:] = []
					destination_ip_print[:] = []
					destination_port_print[:] = []
					all_pack = 1				
				rx_num_flag = 0		
				num_packets = len(s.packets)
				lines = ''
				time_print[:] = []
				flags_print[:] = []
				seq_print[:] = []
				ack_print[:] = []
				tcp_len_print[:] = []
				win_size_print[:] = []
				win_scale_print[:] = []
				dup_ack_num_print[:] = []
				next_seq_print[:] = []
				msg_print[:] = []
				direction_print[:] = []
				st_no_print[:] = []
				frame_number_print[:] = []
				for p in range(0,num_packets) :
					if  stream_number_selected == (counter-1):
						if rx_num_flag == 0 :
							rx_num_flag = 1
							rx_num_dir = str(s.packets[p].rx_num)
						if rx_num_dir == str(s.packets[p].rx_num) :					
							#print ("--->>")
							direction_print.append("--->>")
						else :
							#print ("<<---")
							direction_print.append("<<---")
						st_no_print.append(s.stream_num)
						temp_frame_number = str(s.packets[p].frame_number)					
						frame_number_print.append(temp_frame_number)						
						time_print.append(s.packets[p].frame_time)
						flags_print.append(s.packets[p].flags)
						seq_print.append(s.packets[p].seq_num)
						ack_print.append(s.packets[p].ack_num)
						tcp_len_print.append(s.packets[p].tcp_len)
						win_size_print.append(s.packets[p].win_size)
						win_scale_print.append(s.packets[p].win_scale)
						dup_ack_num_print.append(s.packets[p].dup_ack_num)
						next_seq_print.append(s.packets[p].seq_num)
						msg_print.append(s.packets[p].expert_msg)		
				
					elif not stream_number_filtered.isdigit():
						if rx_num_flag == 0 :
							rx_num_flag = 1
							rx_num_dir = str(s.packets[p].rx_num)
						if rx_num_dir == str(s.packets[p].rx_num) :					
							#print ("--->>")
							direction_print.append("--->>")
						else :
							#print ("<<---")
							direction_print.append("<<---")
						st_no_print.append(s.stream_num)					
						time_print.append(s.packets[p].frame_time)
						flags_print.append(s.packets[p].flags)
						seq_print.append(s.packets[p].seq_num)
						ack_print.append(s.packets[p].ack_num)
						tcp_len_print.append(s.packets[p].tcp_len)
						win_size_print.append(s.packets[p].win_size)
						win_scale_print.append(s.packets[p].win_scale)
						dup_ack_num_print.append(s.packets[p].dup_ack_num)
						next_seq_print.append(s.packets[p].seq_num)
						msg_print.append(s.packets[p].expert_msg)
					
					lines = format_table( [(st_no_print, ALIGN_RIGHT|PADDING_ALL, 'Stream Num'),(time_print, ALIGN_RIGHT|PADDING_ALL, 'Time'),(direction_print, ALIGN_RIGHT|PADDING_ALL, 'DIRECTION'),  (flags_print, ALIGN_LEFT|PADDING_ALL, 'FLAGS'),(seq_print, ALIGN_LEFT|PADDING_ALL, 'Seq'),(ack_print, ALIGN_LEFT|PADDING_ALL, 'Ack'),(tcp_len_print, ALIGN_LEFT|PADDING_ALL, 'tcp_len'),(win_size_print, ALIGN_LEFT|PADDING_ALL, 'Win_Size'),(next_seq_print, ALIGN_LEFT|PADDING_ALL, 'next_seq'),(dup_ack_num_print, ALIGN_LEFT|PADDING_ALL, 'dup_ack_num'),(frame_number_print, ALIGN_LEFT|PADDING_ALL, 'frame_no')] )
				if  stream_number_selected == (counter-1):
					#print all packets of each stream
					print '\n'.join(lines)	
					logging.debug( str('\n'.join(lines)))
				elif not stream_number_filtered.isdigit():
					#print all packets of each stream
					print '\n'.join(lines)	
					logging.debug( str('\n'.join(lines)))					
					
		if all_pack == 0 :
			print '\n'.join(lines_stream)	#print all the streams data
			logging.debug( str('\n'.join(lines_stream)))
		
def populate_data(inputfile,print_option):
	cmd_output = 'random'	
	var = 1	
	x = 0	
	count_stream = 1		
	while var == 1 :
		#command = "tshark -R ' tcp.stream eq " + str(x) + "' -T fields -e tcp.stream -e tcp.scrport -r " + str(inputfile)
		command = "tshark -R ' tcp.stream eq " + str(x) + "' -T fields -e tcp.stream  -e tcp.srcport -e ip.src -e  tcp.dstport -e ip.dst -e nstrace.pdevno -e  nstrace.l_pedevno -e nstrace.dir -e tcp.seq -e tcp.ack -e tcp.len -e tcp.flags -e tcp.window_size_value -e tcp.window_size -e tcp.window_size_scalefactor -e tcp.checksum -e tcp.analysis.duplicate_ack -e tcp.analysis.duplicate_ack_num -e tcp.options.wscale.shift -e tcp.options.sack_perm  -e tcp.options.mss_val -e frame.time_relative -e tcp.nxt.seq -e frame.time_relative -e frame.number -e expert.message  -r " + str(inputfile)
		
		#logging.debug('command gernerated'+ command)
		
		#logging.info('Added Stream " + str(x)	 +" to the Local DB ')
		#logging.warning('And this, too')		
		
		cmd_output = os.popen(command,"r")
		#print cmd_output
		if not cmd_output :
			 break			
		
		stream_flag = 0
		if count_stream == 0 :
			break		
                count_stream = 0
		line_count = 0
		
		while 1:
			line = cmd_output.readline()
			if not line: 
				if line_count != 0:				
					streams.append(stream)							
					#print "added" + str(x)				
				break
			count_stream = count_stream + 1			
			line = line.replace('\t','$')
			output = line.split("$")	
			#print output
			if stream_flag == 0 :
				stream_output = output				
				stream = Stream()
				stream.stream_num = stream_output[0]
				stream.source_ip = stream_output[2]
				stream.destination_ip = stream_output[4]
				stream.source_port = stream_output[1]
				stream.destination_port = stream_output[3]
				stream.ws_val_cl = ''
				stream.mss_val_cl = stream_output[20]
				stream.ws_val_svr = ''
				stream.ws_en = ''		
				stream_flag = 1
				#print "creating string"
			
			packet = Packet()	
			line_count = line_count + 1
			#print "Test"
			packet.frame_number = output[24]			
			packet.frame_time = output[23]
			packet.rx_num = output[7]
			packet.flags = output[11]
			packet.checksum = output[15]
			packet.expert_msg = output[25]
			packet.lpcb_no = output[5]			
			packet.lpcb_no = output[6]
			packet.timestamp = output[21]
			packet.seq_num = output[8]
			packet.ack_num = output[9]
			packet.tcp_len = output[10]
			packet.win_size_cal = output[12]
			packet.dup_ack = output[16]
			packet.dup_ack_num = output[17]
			packet.next_seq = output[22]
			packet.win_size = output[13]
			packet.win_scale = output[14]
			
			stream.packets.append(packet)
			#print "len is"
			#print len(streams)
		
		x = x+1					
	print_data('',print_option)		 		
	
def input_from_file(filename):
	#print "filename is " + sfilename
	inputfile = ''
	outputfile = ''
	filters = ''
	stream_no = ''
	print_option = ''
	testcase = ''
	rto_timeout = ''
	fr_timeout = ''
	#print "here"
	params = {}
	params['inputfile'] = inputfile
	params['outputfile'] = outputfile
	params['filters'] = filters
	params['stream'] = stream_no
	params['testcase'] = testcase
	params['print_option'] = print_option 	
	params['rto_timeout'] = rto_timeout
	params['fr_timeout'] = fr_timeout	

	input_list = []	
	with open(filename,"r") as f:
		for line in f:
			input_list = line.split()
			len_input = len(input_list)			
			if len_input == 3 :			
				if input_list[0] == 'inputfile' : 				
					params['inputfile'] = input_list[2]
				if input_list[0] == 'outputfile' : 				
					params['outputfile'] = input_list[2]
				if input_list[0] == 'filters' : 				
					params['filters'] = input_list[2]
				if input_list[0] == 'stream' : 				
					params['stream'] = input_list[2]
				if input_list[0] == 'testcase' : 				
					params['testcase'] = input_list[2]
				if input_list[0] == 'print_option' : 				
					params['print_option'] = input_list[2]
				if input_list[0] == 'rto_timeout' : 				
					params['rto_timeout'] = input_list[2]
				if input_list[0] == 'fr_timeout' : 				
					params['fr_timeout'] = input_list[2]

	
	if not params['outputfile'] :
		outputfile = time.asctime( time.localtime(time.time()))
	params['outputfile'] = params['outputfile'] + "_log_file"
	params['outputfile'].strip()
	print "\n log file : " + params['outputfile'] + " \n"
	if not params['rto_timeout']:	
		params['rto_timeout'] = 1
	if not params['fr_timeout']:	
		params['fr_timeout'] = 0.030
	#print params	
	return params		



def helper() :
	print "here we will print help"


def do_fast_ret(stream_numb,input_test , fr_timeout):		

	frequency_print = []
	dup_ack_3_time_print = []		
	fr_time_print = []
	flags_print = []
	dseq_print = []
	dack_print = []
	seq_print = []
	ack_print = []
	tcp_len_print = []
	msg_print = []	
	fr_no_print = []
	fr_count = 0		
	result_print = []
	lines = []
	ack_frequency = []	
	frame_number_print = []
	fr_count = 0
	total_passed = 0
	total_failed = 0
	rd3_dup_ack_time = ''
	fr_time = ''	
	dupack_ack = ''
	dupack_seq = ''	
	total_passed = 0
	total_failed = 0
	last_ack_frame = 0
	num = int(stream_numb)	
	stream_len_fr = len(streams[num].packets)
	fr_timeout = float(fr_timeout)

	#direction
	flag_rx_fr = 0
	rx_num_fr = str(streams[num].packets[0].rx_num)		
	if str(input_test) == str(streams[num].source_ip) :
			flag_rx_fr = 1
	#parsing all the packets
	for p1 in range(0,stream_len_fr):

		if ((flag_rx_fr == 1 and rx_num_fr == streams[num].packets[p1].rx_num) or (flag_rx_fr == 0 and rx_num_fr != streams[num].packets[p1].rx_num))and ( int(streams[num].packets[p1].tcp_len) != 0):	
			#print "here is a data packet "
			seq_original = streams[num].packets[p1].seq_num
			ack_original = streams[num].packets[p1].ack_num
			
			seq_ack_packet = int(streams[num].packets[p1].seq_num) + int(streams[num].packets[p1].tcp_len)
			frame_number = streams[num].packets[p1].frame_number
			#print "seq=" + str(seq_original) + "\t\tack=" + str(ack_original)
			#logging.debug(" p =" + str(p1))			
			#logging.debug("seq=" + str(seq_original) + "\t\tack=" + str(ack_original))
			p2 = 0			
			#logging.debug("next packet onward vcxv" + str(frame_number))					
			#logging.debug("next packet onwards" + str(streams[num].packets[p2].frame_number) + "vcxv" + str(frame_number))			
			while str(streams[num].packets[p2].frame_number) != str(frame_number):
				p2 = p2 + 1
			#print "next packet onwards"
			
			
			p2 = p2 + 1			
			p3 = p2
			#print "next packet onwards" 
			#print (streams[num].packets[p2].seq_num)			
			#print "hi"
			#logging.debug("next packet onwards" + str(streams[num].packets[p2].seq_num))
			dup_ack_count = 0
			fr_found = 0		
			
			for p2 in range(p2,stream_len_fr):
				
				if( str(streams[num].packets[p2].seq_num) == str(ack_original) ) and (int(streams[num].packets[p2].ack_num) >= int(seq_ack_packet) ) :
					#got ack for the packet 					
					last_ack_frame = int(streams[num].packets[p2].frame_number)					
					break 		
				seq_number_inside_fr = int(streams[num].packets[p2].seq_num)
				if( int(seq_number_inside_fr) >= int(ack_original) ) and (str(streams[num].packets[p2].ack_num) == str(seq_original) ) and last_ack_frame < int(streams[num].packets[p2].frame_number) :
						#its an dup ack
						#logging.debug("dup ack seq" + str(seq_original)+ "akc " + str(ack_original)  + "dup_ack no" + str(dup_ack_count))								
						dup_ack_count = dup_ack_count + 1			
						
						if int(dup_ack_count) == 3 :
							rd3_dup_ack_time = float(streams[num].packets[p2].frame_time)
							dupack_ack = str(streams[num].packets[p2].ack_num)
							dupack_seq = str(streams[num].packets[p2].seq_num)	
			#logging.debug("have come out here" + str(streams[num].packets[p2].frame_number))
			if int(dup_ack_count) > 2 :
							
				fr_count = fr_count + 1
				#print "fr data prnt"
				
				for p3 in range(p3,stream_len_fr):	
					if( str(streams[num].packets[p3].seq_num) == str(ack_original) ) and (int(streams[num].packets[p3].ack_num) >= int(seq_ack_packet) ) :
						#got ack for the packet
						#logging.debug("packet acked") 					
						break 
			
					if( str(streams[num].packets[p3].seq_num) == str(seq_original) ) and (str(streams[num].packets[p3].ack_num) == str(ack_original)) :

						fr_time = float(streams[num].packets[p3].frame_time)			
						#got fr
						fr_found = 1							
						#print "found fr"	
						#logging.debug("fr found")
						break 
				
				temp_fr_count_print = str(fr_count)				
				fr_no_print.append(temp_fr_count_print)
				temp_3rd_dup_ack_time = str(str(rd3_dup_ack_time))
				dup_ack_3_time_print.append(temp_3rd_dup_ack_time)			
				temp_fr_time_print = str(streams[num].packets[p3].frame_time)				
				fr_time_print.append(temp_fr_time_print)
				flags_print.append(streams[num].packets[p1].flags)
				seq_print.append(streams[num].packets[p1].seq_num)
				ack_print.append(streams[num].packets[p1].ack_num)
				temp_frame_number_print = str(streams[num].packets[p1].frame_number)
				frame_number_print.append(temp_frame_number_print)				
				dseq_print.append(dupack_seq)
				dack_print.append(dupack_ack)						
				temp_dup_ack_count = str(dup_ack_count)
				frequency_print.append(temp_dup_ack_count)
				tcp_len_print.append(streams[num].packets[p1].tcp_len)
				#print str(streams[num].packets[p3].frame_time) + "sd" + str(rd3_dup_ack_time)
				if fr_found  != 0:
					time_diff = float(fr_time) - float(rd3_dup_ack_time)

					msg = (streams[num].packets[p1].expert_msg).split()						
					if msg :
						if str(msg[0]) == "Fast":
							msg = msg[0] + msg [1]	
						else :
							msg = msg[0]	
					msg_print.append(msg)	
					#print time_diff
					if dup_ack_count > 2 and float(time_diff) > fr_timeout :
						#print "fr failed"	
						#logging.debug("fr failed")

						result_print.append("Failed")						
						total_failed = total_failed + 1
					else :		
						#print "passed"
						total_passed = total_passed + 1 
						result_print.append("Passed")						
				else: 
					result_print.append("Failed")						
					total_failed = total_failed + 1
					msg_print.append("")

	lines = format_table( [(fr_no_print, ALIGN_RIGHT|PADDING_ALL, 'FR Num'),(fr_time_print, ALIGN_RIGHT|PADDING_ALL, 'FR Time'),(frame_number_print, ALIGN_RIGHT|PADDING_ALL, 'Frame No'),(dup_ack_3_time_print, ALIGN_RIGHT|PADDING_ALL, '3ack_time'),(flags_print, ALIGN_LEFT|PADDING_ALL, 'FLAGS'),(dseq_print, ALIGN_LEFT|PADDING_ALL, 'Dup_Seq'),(dack_print, ALIGN_LEFT|PADDING_ALL, 'Dup_Ack'),(seq_print, ALIGN_LEFT|PADDING_ALL, 'Seq'),(ack_print, ALIGN_LEFT|PADDING_ALL, 'Ack'),(frequency_print, ALIGN_LEFT|PADDING_ALL, 'Freq'),(result_print, ALIGN_LEFT|PADDING_ALL, 'Result')] )
	if fr_count != 0 :
		print '\n'.join(lines)
		logging.debug( str('\n'.join(lines)))

			
	return (total_passed,total_failed)



def fast_ret(params):	
	passed = 0
	failed = 0
	test_ip = ''
	if not params['fr_timeout'] :
			params['fr_timeout'] = 0.030
	fr_timeout = float(params['fr_timeout'])	
	if not params['stream'] == '' :	
		input_test_ip = raw_input("\nEnter the Test IP \n")
		logging.debug( "\nEnter the Test IP \n")	
		logging.debug( input_test_ip)		
		input_test_ip_list = input_test_ip.split()
		if not input_test_ip_list :	
			print "test ip is wrong "		
			logging.warning('test ip is wrong ')		
			return
		else :
			test_ip = input_test_ip_list[0]
		 	
		number = int(params['stream'])
		
		if not ( streams[number].source_ip == str(test_ip) or streams[number].destination_ip == str(test_ip) ):	
			print "wrong test ip"			
			logging.warning('test ip is wrong ')	
			return		
	
		#execute the test
		print "Stream number : " + str(params['stream'])	
		(total_passed,total_failed) = do_fast_ret(params['stream'],test_ip , fr_timeout)
		passed = total_passed
		failed = total_failed
		print "total passed = " + str(passed) + "total_failed = " + str(failed) 
		logging.info("total passed = " + str(passed) + "total_failed = " + str(failed) )
	else :
		print "checking FR for all the traces"
		logging.info("checking FR for all the traces")
		stream_flag = 0		
		
		for st in streams :
			print "Stream number : " + str(stream_flag)
			input_test_ip = raw_input("\n\n\nEnter the Test IP \n")
			logging.info("Stream number : " + str(stream_flag))
			logging.info(input_test_ip)			
			input_test_ip_list = input_test_ip.split()
			if not input_test_ip_list :	
				print "test ip is wrong "
				logging.warning('"test ip is wrong "')		
				return
			else :
				test_ip = input_test_ip_list[0]
		 	#print str(test_ip) + "test ip is"	

			if str(st.source_ip) == str(test_ip) or (str(st.destination_ip) == str(test_ip)):
				passed = 0
				failed = 0				
				(total_passed,total_failed) = do_fast_ret(stream_flag ,test_ip , fr_timeout)
				passed = total_passed
				failed = total_failed			
				print "\ntotal passed = " + str(passed) + "total_failed = " + str(failed) 
				logging.info("total passed = " + str(passed) + "total_failed = " + str(failed) )
			else :
				print "wrong test ip"				
				logging.warning('"test ip is wrong "')
				return	
			stream_flag = stream_flag + 1





def do_rto(stream_numb,input_test , rto_timeout):		
	rto_time_print = []
	flags_print = []
	seq_print = []
	ack_print = []
	tcp_len_print = []
	msg_print = []	
	rto_no_print = []
	rto_count = 0		
	result_print = []
	original_time_print = []	
	lines = []
	
	frame_number_print = []
	
	total_passed = 0
	total_failed = 0
	
	last_seq_num = 0	

	#all the rto's with time
	all_rto_time = []	
	all_rto_frame = []
	
	rto_flag = ''
	num = int(stream_numb)	
	stream_len_fr = len(streams[num].packets)
	rto_timeout = float(rto_timeout)

	#direction
	flag_rx_fr = 0
	rx_num_fr = str(streams[num].packets[0].rx_num)		
	if str(input_test) == str(streams[num].source_ip) :
			flag_rx_fr = 1
	#parsing all the packets
	for p1 in range(0,stream_len_fr):

		if p1 != 0 :		
			last_seq_num = 	int(streams[num].packets[p1-1].seq_num)
		if ((flag_rx_fr == 1 and rx_num_fr == streams[num].packets[p1].rx_num) or (flag_rx_fr == 0 and rx_num_fr != streams[num].packets[p1].rx_num))and ( int(streams[num].packets[p1].tcp_len) != 0)and(last_seq_num < int(streams[num].packets[p1].seq_num) ):	
			#print "here is a data packet "
			seq_original = streams[num].packets[p1].seq_num
			ack_original = streams[num].packets[p1].ack_num
			rto_flag = streams[num].packets[p1].flags			
			
						
			seq_ack_packet = int(streams[num].packets[p1].seq_num) + int(streams[num].packets[p1].tcp_len)
			frame_number = streams[num].packets[p1].frame_number
			time_original = float(streams[num].packets[p1].frame_time)
			p2 = 0			
				
			while str(streams[num].packets[p2].frame_number) != str(frame_number):
				p2 = p2 + 1

			p2 = p2 + 1			
			p3 = p2
			
			rto_sent_count = 0
			#rto_found = 0		
			all_rto_time[:] = []	
			same_rto_count = 0
			for p2 in range(p2,stream_len_fr):
				
				if( str(streams[num].packets[p2].seq_num) == str(ack_original) ) and (int(streams[num].packets[p2].ack_num) >= int(seq_ack_packet) ) :
					#got ack for the packet 					
					break 		

				seq_number_inside_rto = int(streams[num].packets[p2].seq_num)
				time_inside_rto = float(streams[num].packets[p2].frame_time)
				time_diff_rto = float(time_inside_rto) - float(time_original)	
				if( int(seq_number_inside_rto) == int(seq_original) ) and (str(streams[num].packets	[p2].ack_num) == str(ack_original) ) and (time_diff_rto > rto_timeout ) :
					temp_rto_check_exists = 0
					for temp_rto_check in rto_time_print :			
						if not temp_rto_check == '----':				
							if  float(temp_rto_check) == float(streams[num].packets[p2].frame_time):
								temp_rto_check_exists = 1
					
					if temp_rto_check_exists == 0: 					
						#Its leaving all the repeatative rtos
						#its an rto
						same_rto_count = same_rto_count + 1
						#print " ack seq" + str(seq_original)+ "akc " + str(ack_original)  
						#print "rto is here"
						#store time for all the rto's							
						rto_sent_count = rto_sent_count + 1			
						rto_sent_time = float(streams[num].packets[p2].frame_time)
						all_rto_time.append(rto_sent_time)				
						all_rto_frame.append(str(streams[num].packets[p2].frame_number))
						if same_rto_count == 1 and time_diff_rto < (2*rto_timeout) :	
							result_print.append("passed")
							total_passed = total_passed + 1
						elif same_rto_count == 2 and time_diff_rto < (4*rto_timeout) and time_diff_rto > (2*rto_timeout) :
							result_print.append("passed")	
							total_passed = total_passed + 1

						elif same_rto_count == 3 and time_diff_rto < (8*rto_timeout) and time_diff_rto > (3*rto_timeout) :
							result_print.append("passed")	
							total_passed = total_passed + 1

						elif same_rto_count == 4 and time_diff_rto < (16*rto_timeout) and time_diff_rto > (4*rto_timeout) :
							result_print.append("passed")	
							total_passed = total_passed + 1

						elif same_rto_count == 5 and time_diff_rto < (32*rto_timeout) and time_diff_rto > (5*rto_timeout) :
							result_print.append("passed")	
							total_passed = total_passed + 1

						elif same_rto_count == 6 and time_diff_rto < (64*rto_timeout) and time_diff_rto > (6*rto_timeout) :
							result_print.append("passed")	
							total_passed = total_passed + 1
						elif same_rto_count == 7 and time_diff_rto < (128*rto_timeout) and time_diff_rto > (7*rto_timeout) :
							result_print.append("passed")	
							total_passed = total_passed + 1
						else :	
							total_failed = total_failed + 1					
							result_print.append("failed")
				if rto_sent_count == 8:
					# 7RTO's sent so it shd sent RST				
					#print "RTO shd be sent"
					break
				
			#logging.debug("have come out here" + str(streams[num].packets[p2].frame_number))
			
			if rto_sent_count > 0 :
				rto_count = rto_count + 1			
				#print got rto			
				for all_rto in range(0,rto_sent_count) :
					temp_rto_count_print = str(rto_count)				
					rto_no_print.append(temp_rto_count_print)
						
					temp_rto_time_print = str(all_rto_time[all_rto])
					rto_time_print.append(temp_rto_time_print)	

					temp_rto_frame_print = str(all_rto_frame[all_rto])	
					frame_number_print.append(temp_rto_frame_print)
	
					temp_original_time = str(time_original)					
					original_time_print.append(temp_original_time)					
					seq_print.append(str(seq_original))
					ack_print.append(str(ack_original))
					flags_print.append(rto_flag)					
					

				
				#print "separating the rto's"
				rto_no_print.append("----")
				rto_time_print.append("----")
				flags_print.append("----")				
				frame_number_print.append("----")
				original_time_print.append("----")					
				seq_print.append("----")
				ack_print.append("----")
				result_print.append("----")			
	lines = format_table( [(rto_no_print, ALIGN_RIGHT|PADDING_ALL, 'RTO Num'),(rto_time_print, ALIGN_RIGHT|PADDING_ALL, 'RTO Time'),(frame_number_print, ALIGN_RIGHT|PADDING_ALL, 'Frame No'),(original_time_print, ALIGN_RIGHT|PADDING_ALL, 'original_time'),(flags_print, ALIGN_LEFT|PADDING_ALL, 'FLAGS'),(seq_print, ALIGN_LEFT|PADDING_ALL, 'Seq'),(ack_print, ALIGN_LEFT|PADDING_ALL, 'Ack'),(result_print, ALIGN_LEFT|PADDING_ALL, 'Result')] )
	if rto_count != 0 :
		print "inside"		
		print '\n'.join(lines)
		logging.debug( str('\n'.join(lines)))

			
	return (total_passed,total_failed)


		


def rto(params):	
	passed = 0
	failed = 0
	test_ip = ''
	if not params['rto_timeout'] :
			params['rto_timeout'] = 0.2

	rto_timeout = float(params['rto_timeout'])	
	if not params['stream'] == '' :	
		input_test_ip = raw_input("\nEnter the Test IP \n")
		logging.debug( "\nEnter the Test IP \n")	
		logging.debug( input_test_ip)		
		input_test_ip_list = input_test_ip.split()
		if not input_test_ip_list :	
			print "test ip is wrong "		
			logging.warning('test ip is wrong ')		
			return
		else :
			test_ip = input_test_ip_list[0]
		 	
		number = int(params['stream'])
		
		if not ( streams[number].source_ip == str(test_ip) or streams[number].destination_ip == str(test_ip) ):	
			print "wrong test ip"			
			logging.warning('test ip is wrong ')	
			return		
	
		#execute the test
		print "Stream number : " + str(params['stream'])	
		(total_passed,total_failed) = do_rto(params['stream'],test_ip , rto_timeout)
		passed = total_passed
		failed = total_failed
		print "total passed = " + str(passed) + "total_failed = " + str(failed) 
		logging.info("total passed = " + str(passed) + "total_failed = " + str(failed) )
	else :
		print "checking FR for all the traces"
		logging.info("checking FR for all the traces")
		stream_flag = 0		
		
		for st in streams :
			print "Stream number : " + str(stream_flag)
			input_test_ip = raw_input("\n\n\nEnter the Test IP \n")
			logging.info("Stream number : " + str(stream_flag))
			logging.info(input_test_ip)			
			input_test_ip_list = input_test_ip.split()
			if not input_test_ip_list :	
				print "test ip is wrong "
				logging.warning('"test ip is wrong "')		
				return
			else :
				test_ip = input_test_ip_list[0]
		 	#print str(test_ip) + "test ip is"	

			if str(st.source_ip) == str(test_ip) or (str(st.destination_ip) == str(test_ip)):
				passed = 0
				failed = 0				
				(total_passed,total_failed) = do_rto(stream_flag ,test_ip , rto_timeout)
				passed = total_passed
				failed = total_failed			
				print "\ntotal passed = " + str(passed) + "total_failed = " + str(failed) 
				logging.info("total passed = " + str(passed) + "total_failed = " + str(failed) )
			else :
				print "wrong test ip"				
				logging.warning('"test ip is wrong "')
				return	
			stream_flag = stream_flag + 1
			







def run_time(params):
	while(1) :
		input_data = raw_input("\nEnter the new command \n")
		if( input_data.find("exit") != -1 ):
			print "exiting !!!!!!"			
			sys.exit()
		logging.debug( input_data )
		input_data_list = input_data.split()
		#help
		filter_update = '-h'
		filter_update_alis = '--help'			
		if( (filter_update in input_data_list)or( filter_update_alis in input_data_list) ) :
			helper()					
			continue
		#RTO
		filter_update = '-rto'
		filter_update_alis = '--rto_timeout'
		if( (filter_update in input_data_list)or( filter_update_alis in input_data_list) ) :
			index_filter = input_data_list.index(filter_update)
			try:			
				params['rto_timeout'] = float(input_data_list[ index_filter + 1])
				stream_update_val = 1			
				
			except :
				print "!!RTO is not entered !!"				
				pass
			
		#FR 
		filter_update = '-fr_timeout'
		filter_update_alis = '--fr_timeout'
		if( (filter_update in input_data_list)or( filter_update_alis in input_data_list) ) :
			index_filter = input_data_list.index(filter_update)
			try:			
				params['fr_timeout'] = float(input_data_list[ index_filter + 1])
				stream_update_val = 1			
				
			except :
				print "!!FR_timeout is not entered !!"				
				pass


		#filters
		filter_update_val = 0	
		filter_update = '-f'
		filter_update_alis = '--filters'			
		if( (filter_update in input_data_list)or( filter_update_alis in input_data_list) ) :
			index_filter = input_data_list.index(filter_update)
			#name of the filter is no there				
			try:
				filter_str = input_data_list[ index_filter + 1] + " " +input_data_list[ index_filter + 2] + "  " + input_data_list[ index_filter + 3]				
				params['filters'] = filter_str
				filter_update_val = 1				
				#print "params['filter']" + params['filters'] + "updated"
			except :
				print "!!filter name is not entered !!"					
				pass	
		#stream
		stream_update_val = 0
		filter_update = '-s'
		filter_update_alis = '--stream'
		if( (filter_update in input_data_list)or( filter_update_alis in input_data_list) ) :
			index_filter = input_data_list.index(filter_update)
			try:			
				params['stream'] = input_data_list[ index_filter + 1]
				stream_update_val = 1			
				if int(params['stream']) > len(streams) or int(params['stream']) < 0 or not params['stream'].isdigit():
					print "<!!stream out of bounds!!> \n"
				#print "params['stream']" + params['stream'] + "updated"	
					continue 
			except :
				print "!!stream name is not entered !!"				
				pass
			
		#print option
		filter_update = '-p'		
		filter_update_alis = '--print_option'	
		if( (filter_update in input_data_list)or( filter_update_alis in input_data_list) ) :
			index_filter = input_data_list.index(filter_update)
			try :
				params['print_option'] = input_data_list[ index_filter + 1]
				print "params['print_option']" + str(params['print_option']) + "updated"
			except :
				print "!!filter name is not entered !!"
				pass				
		#testcase
		filter_update = '-t'
		filter_update_alis = '--stream'			
		if filter_update_val == 1 and stream_update_val == 1 :
			print "<!!stream and filter cannot be used together !!>"		
		elif( (filter_update in input_data_list)or( filter_update_alis in input_data_list) ) :
			index_filter = input_data_list.index(filter_update)
			#print "params['print_option']" + params['print_option'] + "updated"
			params['testcase'] = input_data_list[ index_filter + 1]
			if(( params['testcase'] == "FR")or( params['testcase'] == "fr")):
				fast_ret(params)
			elif(( params['testcase'] == "RTO")or( params['testcase'] == "rto")):	
				rto(params)
			
		elif stream_update_val == 1:
			print_data(int(params['stream']),params['print_option'])
		
		elif filter_update_val == 1 :
				#print "printing filter" + str(params['filters']) 			
				filter_stream(params['filters'],str(params['print_option']))
		else :
			print "!!wrong input!!"
		params['filters'] = ''
		params['stream'] = ''
		params['testcase'] = ''
		params['print_option'] = ''			
		params['rto_timeout'] = ''		
		params['fr_timeout'] = ''		

if __name__ == "__main__":	
	if  len(sys.argv) < 2 :
		print "\n\t\t<usuage : python tracetool.py input_filename>\n"	
		sys.exit()
	params = input_from_file(sys.argv[1])
	logging.basicConfig(filename=params['outputfile'],level=logging.DEBUG)	
	populate_data(params['inputfile'],params['print_option'])
	run_time(params)	


	

