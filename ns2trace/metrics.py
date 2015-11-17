__author__= "barun"
__date__  = "$20 May, 2011 12:19:25 PM$"


## Defines a collection of metrics that can be used to analyze the performance
#  of a network.
class Metrics(object):
        
    
    ## Calculate average throughput as: total_bytes_rcvd / duration.
    #
    #  @param pkts_list An iterator object in the format [(timestamp, size),]
    #  @param duration Time duration (in s) over which thruput is to be computed. Typically it is the simulation period.
    #  @return Average throughput in Kbps; return -1 if duration is not positive
    @staticmethod
    def average_throughput(pkts_list, duration):
        #print 'Average throughput'
        avg_thruput = 0
        start = -1
        stop = 0
        
        if pkts_list:            
            for record in pkts_list:
                #print record
                try:
                    avg_thruput += long(record[1])
                    if start == -1:
                        start = float(record[0])
                    stop = float(record[0])
                    #print record[0], record[1]
                except IndexError:
                    pass

            if duration <= 0:
                duration = stop - start + 0.00000001
                
            #print 'duration:', duration
            avg_thruput = 8 * float(avg_thruput) / (1024 * duration)     # Since pkt len is in bytes

        return avg_thruput


    @staticmethod
    ## Calculate instantaneous throughput as total bytes_rcvd at each time instant.
    #
    #  <b>Logic</b>: To determine total bytes received at any instant, say, at t = 5, sum
    #  up sizes of all packets received in the interval 5.00000... to 5.99999...
    #
    #  This procedure is repeated for all the time instances.
    #  @param pkts_list An iterator object in the format [(timestamp, size),]
    #  @return A list in the form [(time_instance, total_Kbytes),]
    def instantaneous_throughput(pkts_list=None):
        #print 'Instantaneous throughput'

        result = []
        start_time = -1     # Anything less than 0
        this_instance = 0
        bytes_this_instance = 0
        #i_duration = long(duration)

        if pkts_list:
            for record in pkts_list:
                try:
                    if start_time < 0:      # This is the first record encountered
                        start_time = float(record[0])
                        #print start_time
                        this_instance = int(start_time)
                        #print this_instance
                        bytes_this_instance = long(record[1])
                        continue

                    cur_time = float(record[0])
                    if this_instance < cur_time and\
                        cur_time < (this_instance + 1):                            
                            bytes_this_instance += long(record[1])
                    else:
                        result.append( (this_instance, bytes_this_instance * 8 / 1024) )
                        this_instance += 1
                        bytes_this_instance = long(record[1])
                except IndexError:
                    pass

            # Append the last record
            result.append( (this_instance, bytes_this_instance * 8 / 1024) )
            
        return result


    @staticmethod
    def cumulative_bytes_received(pkts_list=None):
        #print 'Cumulative plot of bytes received'

        result = []
        start_time = -1     # Anything less than 0
        this_instance = 0
        bytes_this_instance = 0

        if pkts_list:
            for record in pkts_list:
                try:
                    if start_time < 0:
                        start_time = float(record[0])
                        this_instance = int(start_time)
                        bytes_this_instance = long(record[1])                        
                        continue

                    cur_time = float(record[0])
                    bytes_this_instance += long(record[1])

                    if this_instance < cur_time and\
                        cur_time < (this_instance + 1):
                            continue
                    else:                        
                        result.append( (this_instance, ( float(bytes_this_instance / 1024)  ) * 8 ) )
                        this_instance += 1
                        #print cur_time
                except IndexError:
                    pass
            # Append the last record
            result.append( (this_instance, ( float(bytes_this_instance / 1024)  ) * 8 ) )

        return result


    @staticmethod
    ## Calculate throughput as total bytes_rcvd upto current instance of time / total duration upto current instance
    #  @param pkts_list An iterator object in the format [(timestamp, size),]
    #  @return A list in the form [(time_instance, total_bytes),]
    def cumulative_throughput(pkts_list=None):
        #print 'Current throughput'

        result = []
        start_time = -1     # Anything less than 0
        this_instance = 0
        bytes_this_instance = 0

        if pkts_list:
            for record in pkts_list:
                try:
                    if start_time < 0:
                        start_time = float(record[0])
                        this_instance = int(start_time)
                        bytes_this_instance = long(record[1])                        
                        continue

                    cur_time = float(record[0])
                    bytes_this_instance += long(record[1])
                                        
                    if this_instance < cur_time and\
                        cur_time < (this_instance + 1):
                            continue
                    else:                        
                        result.append( (this_instance, ( float(bytes_this_instance / 1024) / ( this_instance - int(start_time) + 1) ) * 8 ) )
                        this_instance += 1
                except IndexError:
                    pass
            # Append the last record
            result.append( (this_instance, ( float(bytes_this_instance / 1024) / ( this_instance - int(start_time) + 1) ) * 8 ) )

        return result

    
    ## Return the end to end delay for each packet moving between a source and
    #  destination node, and identified by a flow ID. The delay is computed as
    #  the difference between sending time of the packet at source node and
    #  receiving time of the packet at the destination node.
    #  @param send_pkts_list An iterator object in the format [(seq_num, timestamp)]
    #  @param rcvd_pkts_list An iterator object in the format [(seq_num, timestamp)]
    #  @return A list in the form [(seq_num, delay),]
    @staticmethod
    def end2end_delay(send_pkts_list=None, rcvd_pkts_list=None):
        #print 'End to end delay'

        send_pkts = {}
        rcvd_pkts = {}

        for pkt in send_pkts_list:
            send_pkts[pkt[0]] = float(pkt[1])
      
        for pkt in rcvd_pkts_list:
            rcvd_pkts[pkt[0]] = float(pkt[1])
        
        pkt_delay = []

        for seq_num in send_pkts:
            if seq_num in rcvd_pkts:
                if rcvd_pkts[seq_num] >= send_pkts[seq_num]:
                    delay = rcvd_pkts[seq_num] - send_pkts[seq_num]
                    pkt_delay.append( (seq_num, delay) )

        # Sort pkt_delay in integer order of seq_num -- otherwise displayed
        # graph would be garbage
        pkt_delay = [ ( int(e[0]), e[1], ) for e in pkt_delay ]
        pkt_delay.sort()
        
        return pkt_delay

    #  @param send_pkts_list An iterator object in the format [seq_num]
    @staticmethod
    def packet_retransmissions(send_pkts_list=None):
        #print 'Packet retransmissions'

        send_pkts = {}

        send_pkts_list = [ int(item) for item in send_pkts_list ]
        
        for seq_num in send_pkts_list:
            if seq_num in send_pkts:
                send_pkts[seq_num] += 1
            else:
                send_pkts[seq_num] = 0

        pkt_retransmits = []

        for (seq_num, retransmits) in send_pkts.items():
            if retransmits != 0:
                pkt_retransmits.append( (seq_num, retransmits) )

        pkt_retransmits.sort()
        return pkt_retransmits
