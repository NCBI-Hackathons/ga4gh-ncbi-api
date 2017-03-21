import re
from ngs.Alignment import Alignment
from ga4gh.schemas import protocol
from ga4gh.schemas.ga4gh import common_pb2
from ga4gh.schemas.ga4gh import reads_pb2

""" Mapping of cigar operator code to CigarUnit """
cigarOp = {'M': protocol.CigarUnit.ALIGNMENT_MATCH,
           'I': protocol.CigarUnit.INSERT,
           'D': protocol.CigarUnit.DELETE,
           'N': protocol.CigarUnit.SKIP,
           'S': protocol.CigarUnit.CLIP_SOFT,
           'H': protocol.CigarUnit.CLIP_HARD,
           'P': protocol.CigarUnit.PAD,
           '=': protocol.CigarUnit.SEQUENCE_MATCH,
           'X': protocol.CigarUnit.SEQUENCE_MISMATCH}


def num_reads(align):
    """ Returns the number of reads in the template 
    
    Args:
        align (ngs.Alignment): aligned read
        
    Returns:
        int: the number of reads in the template
        
    """
    if align.hasMate():
        return(2)
    else:
        return(1)
    

def strand(align):
    try:
        if align.getIsReversedOrientation():
            return(common_pb2.NEG_STRAND)
        else:
            return(common_pb2.POS_STRAND)
    except Exception:
        return(common_pb2.STRAND_UNSPECIFIED)
    

def setCigar(read_align, cigar_str):
    if re.match(r'^([0-9]+[MIDNSHPX=])+$', cigar_str) != None:
        units = re.findall(r'([0-9]+)([MIDNSHPX=])', cigar_str)
        ref = read_align.alignment.position.reference_name
        if ref == "":
            raise RuntimeError('Reference name not set')
        for length, op in units:
            cigarUnit = read_align.alignment.cigar.add()
            cigarUnit.operation = cigarOp[op]
            cigarUnit.operation_length = long(length)
            cigarUnit.reference_sequence = ref
        

def ngs2ga4gh(align):
    ref = align.getReferenceSpec() # The reference sequence
    rtrn = protocol.ReadAlignment() # GA4GH object to return
    rtrn.id = align.getAlignmentId() # Unique within read collection
    rtrn.read_group_id = align.getReadGroup()
    rtrn.fragment_name = align.getFragmentId() # Alignment extends Fragment. A "Fragment" is an individual read.
    #rtrn.improper_placement = ???
    #rtrn.duplicate_fragment = ???
    rtrn.number_reads = num_reads(align)
    #rtrn.fragment_length = ???
    #rtrn.read_number = NOT AVAILABLE THROUGH NGS
    #rtrn.failed_vendor_quality_checks = NOT AVAILABLE THROUGH NGS
    rtrn.alignment.position.reference_name = ref
    rtrn.alignment.position.position = align.getAlignmentPosition() # Both zero-based
    rtrn.alignment.position.strand = strand(align)
    rtrn.alignment.mapping_quality = align.getMappingQuality()
    setCigar(rtrn, align.getLongCigar(False))
    rtrn.secondary_alignment = align.getAlignmentCategory() == Alignment.secondaryAlignment
    #rtrn.supplementary_alignment = NOT AVAILABLE THROUGH NGS
    rtrn.aligned_sequence = align.getClippedFragmentBases()
    #rtrn.aligned_quality = ???
    if rtrn.number_reads > 1:
        mate_align = align.getMateAlignment()
        rtrn.next_mate_position.reference_name = mate_align.getReferenceSpec()
        rtrn.next_mate_position.position = mate_align.getAlignmentPosition()
        rtrn.next_mate_position.strand = strand(mate_align)
    #rtrn.attributes = ???
    return(rtrn)
    


