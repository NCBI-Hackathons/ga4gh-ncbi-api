import align_conv
from ngs import NGS
from ngs.Alignment import Alignment

acc = 'SRR2856889' # paired
#acc = 'SRR1482462' # unpaired
refName = 'chr1'
start = 9000000
stop = 9100000


def run(acc, refName, start, stop):
    # open requested accession using SRA implementation of the API
    with NGS.openReadCollection(acc) as run:
        run_name = run.getName()
    
        # get requested reference
        with run.getReference(refName) as ref:
            # start iterator on requested range
            with ref.getAlignmentSlice(start, stop-start+1, Alignment.primaryAlignment) as it:
                i = 0
                while it.nextAlignment():
                    align = align_conv.ngs2ga4gh(it)
                    print("""
                    id:\t%s
                    read_group_id:\t%s
                    fragment_name:\t%s
                    improper_placement:\t%s
                    duplicate_fragment:\t%s
                    number_reads:\t%s
                    fragment_length:\t%s
                    read_number:\t%s
                    failed_vendor_quality_checks:\t%s
                    alignment.position.reference_name:\t%s
                    alignment.position.position:\t%s
                    alignment.position.strand:\t%s
                    alignment.mapping_quality:\t%s
                    alignment.cigar:\t%s
                    secondary_alignment:\t%s
                    supplementary_alignment:\t%s
                    aligned_sequence:\t%s
                    aligned_quality:\t%s
                    next_mate_position.reference_name:\t%s
                    next_mate_position.position:\t%s
                    next_mate_position.strand:\t%s
                    attributes:\t%s
                    """ % 
                          (align.id, 
                            align.read_group_id,
                            align.fragment_name,
                            align.improper_placement,
                            align.duplicate_fragment,
                            align.number_reads,
                            align.fragment_length,
                            align.read_number,
                            align.failed_vendor_quality_checks,
                            align.alignment.position.reference_name,
                            align.alignment.position.position,
                            align.alignment.position.strand,
                            align.alignment.mapping_quality,
                            align.alignment.cigar,
                            align.secondary_alignment,
                            align.supplementary_alignment,
                            align.aligned_sequence,
                            align.aligned_quality,
                            align.next_mate_position.reference_name,
                            align.next_mate_position.position,
                            align.next_mate_position.strand,
                            align.attributes
                           ))
                    i += 1
                print ("Read {} alignments for {}".format(i, run_name))



run(acc, refName, start, stop)



