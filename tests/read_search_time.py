import timeit
        
def time(acc, ref, start, end, pg_size, pg_token):
    timer = timeit.Timer('ncbi.search_reads(request)', setup = """from ga4gh.schemas import protocol; 
import ncbi; 
request = protocol.SearchReadsRequest(); 
request.reference_id = '%s'; 
request.read_group_ids.extend(['%s']); 
request.start = %s; 
request.end = %s; 
request.page_size = %s; 
request.page_token = '%s'""" % (ref, acc, start, end, pg_size, pg_token))
    print('%s\t%s:%s-%s\tpage_size=%s\tpage_token=%s\ttime=%s' % (acc, ref, start, end, pg_size, pg_token, timer.timeit(1)))



time(acc='SRR2856889', ref='chr1', start=9000000, end=9050000, pg_size=100, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9100000, pg_size=100, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9500000, pg_size=100, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=10000000, pg_size=100, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=20000000, pg_size=100, pg_token='')

time(acc='SRR2856889', ref='chr1', start=9000000, end=9050000, pg_size=1000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9100000, pg_size=1000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9500000, pg_size=1000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=10000000, pg_size=1000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=20000000, pg_size=1000, pg_token='')

time(acc='SRR2856889', ref='chr1', start=9000000, end=9050000, pg_size=10000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9100000, pg_size=10000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9500000, pg_size=10000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=10000000, pg_size=10000, pg_token='')
time(acc='SRR2856889', ref='chr1', start=9000000, end=20000000, pg_size=10000, pg_token='')

time(acc='SRR2856889', ref='chr1', start=9000000, end=9050000, pg_size=100, pg_token='9025000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9100000, pg_size=100, pg_token='9050000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9500000, pg_size=100, pg_token='9250000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=10000000, pg_size=100, pg_token='9500000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=20000000, pg_size=100, pg_token='10000000')

time(acc='SRR2856889', ref='chr1', start=9000000, end=9050000, pg_size=1000, pg_token='9025000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9100000, pg_size=1000, pg_token='9050000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9500000, pg_size=1000, pg_token='9250000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=10000000, pg_size=1000, pg_token='9500000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=20000000, pg_size=1000, pg_token='10000000')

time(acc='SRR2856889', ref='chr1', start=9000000, end=9050000, pg_size=10000, pg_token='9025000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9100000, pg_size=10000, pg_token='9050000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=9500000, pg_size=10000, pg_token='9250000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=10000000, pg_size=10000, pg_token='9500000')
time(acc='SRR2856889', ref='chr1', start=9000000, end=20000000, pg_size=10000, pg_token='10000000')



