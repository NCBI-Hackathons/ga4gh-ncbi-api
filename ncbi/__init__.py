import re
from ngs import NGS
from ngs.Alignment import Alignment
from ga4gh.schemas import protocol
from ga4gh.schemas.ga4gh import common_pb2
import requests
import xml.etree.ElementTree as ET

# Mapping of cigar operator code to CigarUnit
_CIGAR_OPERATION_MAP = {'M': protocol.CigarUnit.ALIGNMENT_MATCH,
           'I': protocol.CigarUnit.INSERT,
           'D': protocol.CigarUnit.DELETE,
           'N': protocol.CigarUnit.SKIP,
           'S': protocol.CigarUnit.CLIP_SOFT,
           'H': protocol.CigarUnit.CLIP_HARD,
           'P': protocol.CigarUnit.PAD,
           '=': protocol.CigarUnit.SEQUENCE_MATCH,
           'X': protocol.CigarUnit.SEQUENCE_MISMATCH}

# Default page size
_DEFAULT_PAGE_SIZE = 1000

def _get_num_reads(ngs_alignment):
    """ Returns the number of reads in the template of an NCBI/NGS alignment

    Args:
        ngs_alignment (ngs.Alignment): aligned read

    Returns:
        int: the number of reads in the template

    """
    if ngs_alignment.hasMate():
        return(2)
    else:
        return(1)


def _get_strand(ngs_alignment):
    """ Returns the strand of an NCBI/NGS alignment
    
    Args:
        ngs_alignment (ngs.Alignment): aligned read

    Returns:
        GA4GH Strand
    
    """
    try:
        if ngs_alignment.getIsReversedOrientation():
            return (common_pb2.NEG_STRAND)
        else:
            return (common_pb2.POS_STRAND)
    except Exception:
        return (common_pb2.STRAND_UNSPECIFIED)


def _set_cigar(ga_alignment, cigar_str):
    """
    Mutates a ga4gh alignment protobuf to
    add cigar elements using the `cigar_str`.
    """
    if re.match(r'^([0-9]+[MIDNSHPX=])+$', cigar_str) != None:
        units = re.findall(r'([0-9]+)([MIDNSHPX=])', cigar_str)
        ref = ga_alignment.alignment.position.reference_name
        if ref == "":
            raise RuntimeError('Reference name not set')
        for length, op in units:
            try:
                cigarUnit = ga_alignment.alignment.cigar.add()
                cigarUnit.operation = _CIGAR_OPERATION_MAP[op]
                cigarUnit.operation_length = long(length)
                cigarUnit.reference_sequence = ref
            except Exception:
                # Safely set the cigar operations
                pass


def _convert_alignment(ngs_alignment):
    """
    Accepts an NCBI/NGS alignment and returns a GA4GH ReadAlignment
    protobuf.
    """
    reference_name = ngs_alignment.getReferenceSpec()  # The reference sequence
    ga_alignment = protocol.ReadAlignment()  # GA4GH object to return
    ga_alignment.id = ngs_alignment.getAlignmentId()  # Unique within read collection
    ga_alignment.read_group_id = ngs_alignment.getReadGroup()
    # Alignment extends Fragment. A "Fragment" is an individual read.
    ga_alignment.fragment_name = ngs_alignment.getFragmentId()
    # rtrn.improper_placement = ???
    # rtrn.duplicate_fragment = ???
    ga_alignment.number_reads = _get_num_reads(ngs_alignment)
    # rtrn.fragment_length = ???
    # rtrn.read_number = NOT AVAILABLE THROUGH NGS
    # rtrn.failed_vendor_quality_checks = NOT AVAILABLE THROUGH NGS
    ga_alignment.alignment.position.reference_name = reference_name
    ga_alignment.alignment.position.position = ngs_alignment.getAlignmentPosition()  # Both zero-based
    ga_alignment.alignment.position.strand = _get_strand(ngs_alignment)
    ga_alignment.alignment.mapping_quality = ngs_alignment.getMappingQuality()
    _set_cigar(ga_alignment, ngs_alignment.getLongCigar(False))
    ga_alignment.secondary_alignment = ngs_alignment.getAlignmentCategory() == Alignment.secondaryAlignment
    # rtrn.supplementary_alignment = NOT AVAILABLE THROUGH NGS
    ga_alignment.aligned_sequence = ngs_alignment.getClippedFragmentBases()
    # rtrn.aligned_quality = ???
    if ga_alignment.number_reads > 1:
        mate_align = ngs_alignment.getMateAlignment()
        ga_alignment.next_mate_position.reference_name = mate_align.getReferenceSpec()
        ga_alignment.next_mate_position.position = mate_align.getAlignmentPosition()
        ga_alignment.next_mate_position.strand = _get_strand(mate_align)
    # rtrn.attributes = ???
    return(ga_alignment)

def _print_ga_alignment(ga_alignment):
    """
    Used for debugging.
    """
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
          (ga_alignment.id,
           ga_alignment.read_group_id,
           ga_alignment.fragment_name,
           ga_alignment.improper_placement,
           ga_alignment.duplicate_fragment,
           ga_alignment.number_reads,
           ga_alignment.fragment_length,
           ga_alignment.read_number,
           ga_alignment.failed_vendor_quality_checks,
           ga_alignment.alignment.position.reference_name,
           ga_alignment.alignment.position.position,
           ga_alignment.alignment.position.strand,
           ga_alignment.alignment.mapping_quality,
           ga_alignment.alignment.cigar,
           ga_alignment.secondary_alignment,
           ga_alignment.supplementary_alignment,
           ga_alignment.aligned_sequence,
           ga_alignment.aligned_quality,
           ga_alignment.next_mate_position.reference_name,
           ga_alignment.next_mate_position.position,
           ga_alignment.next_mate_position.strand,
           ga_alignment.attributes))

def search_datasets(request):
    # TODO safely cast page token
    page_size = 100  # Default page size
    if request.page_size != 0:
        page_size = request.page_size
    page_token = 0
    if request.page_token != '':
        page_token = int(request.page_token)
    offset = page_token * request.page_size
    esearch_params = {
        'db': 'bioproject',
        'term': 'all[filter]',
        'retmax': page_size,
        'retstart': offset
    }
    esearch_response = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        esearch_params)
    # get IDs
    ids = []
    root = ET.fromstring(esearch_response.text)
    for id_ in root.findall("./IdList/Id"):
        ids.append(id_.text)
    # get summaries
    esummary_params = {'db': 'bioproject', 'id': ','.join(ids)}
    esummary_response = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        params=esummary_params)
    root = ET.fromstring(esummary_response.text.encode('utf-8'))
    dataset_list = []
    for ds in root.findall("./DocumentSummarySet/DocumentSummary"):
        dataset = protocol.Dataset()
        # uid = ds.find('Project_Id').text
        dataset.id = ds.find('Project_Acc').text  # id
        dataset.name = ds.find('Project_Title').text  # name
        dataset.description = ds.find('Project_Description').text
        dataset_list.append(dataset)
    return dataset_list

def search_reads(request):
    """ Searches a genomic interval in the NCBI API and returns a list of converted GA4GH alignments
    
    Args:
        request: SearchReadsRequest. If `request.page_size` is set, up to this many records are returned.
                 If not set, `_DEFAULT_PAGE_SIZE` is used as the page size.
                 `request.start` can be overridden by providing a greater start position in `request.page_token`.
                 If provided, `request.page_token` is parsed to a long and compared with `request.start`. 
                 In that case, the greater of the two is used as the zero-based inclusive interval start.
    
    Returns:
        Tuple:
            1) List of converted alignments in GA4GH schema
            2) Maximum zero-based exclusive alignment end position over all alignments returned.
               This value can be set as request.page_token (after parsing to a string) for a subsequent
               request; in that case, streaming will pick up where it left off after this request.
    
    """
    # We are assuming the read group IDs are singleton
    run_accession = request.read_group_ids[0]
    reference_name = request.reference_id
    # Choose the start position between request.start and request.page_token
    try:
        start = max(long(request.page_token), request.start)
    except ValueError:
        start = request.start
    end = request.end
    # Number of alignments to get
    if request.page_size < 1:
        num_aligns = _DEFAULT_PAGE_SIZE
    else:
        num_aligns = request.page_size

    alignments = []
    max_aligned_pos = 0 # Keep track of max zero-based exclusive alignment end
    # open requested accession using SRA implementation of the API
    with NGS.openReadCollection(run_accession) as run:
        # get requested reference
        with run.getReference(reference_name) as reference:
            # start iterator on requested range
            # We need to find out if it returns overlapping reads, or just
            # those that fit within the slice.
            with reference.getAlignmentSlice(start, end - start + 1,
                                       Alignment.primaryAlignment) as it:
                i = 0
                while it.nextAlignment():
                    # Only get the requested number of alignments
                    if i == num_aligns:
                        break
                    max_aligned_pos = max(max_aligned_pos, it.getAlignmentPosition() + it.getAlignmentLength())
                    ga_alignment = _convert_alignment(it)
                    alignments.append(ga_alignment)
                    i += 1
    return (alignments, max_aligned_pos)
