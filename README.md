# GA4GH NCBI API

Genomic data is often very large and requires metadata in order to be used as
part of an inquiry. To make the process of discovering and analyzing genomic
data less of a challenge, the Global Alliance for Genomics and Health (GA4GH)
has designed an "easy-to-implement" HTTP API that lets you get at just the data
relevant to a specific inquiry.

The National Center for Biotechnology Information (NCBI) curates a great deal
of invaluable genomic data. By making these data available using GA4GH methods
the NCBI data becomes discoverable using GA4GH HTTP Clients.

[Draft Manuscript](https://docs.google.com/document/d/170xIZ2v9ciM704T4tCXWQHz71kV9kkXS3qdlgtRxb7U/edit?usp=sharing)

## Installation

Install python

Install pip

Install virtualenvironment

Install NGS

## Running via docker

Give docker pull instructions and details

## Example usage

link to notebook

## GA4GH Schemas

The GA4GH has designed a schema in Google Protocol Buffers which provides the
data serialization and de-serialization layers for this application.

## What is protocol buffers

### Dataset Service

Allows one to interrogate about the containing project used for collecting a genomics dataset.

[Description of Dataset](http://ga4gh-schemas.readthedocs.io/en/latest/api/metadata.html#dataset)

[Source documentation](http://ga4gh-schemas.readthedocs.io/en/latest/schemas/metadata_service.proto.html)

### Read Service

Allows one to interrogate about the metadata regarding a run, as well as the underlying alignments.

[Description of Read Service](http://ga4gh-schemas.readthedocs.io/en/latest/schemas/read_service.proto.html)

[Source documentation](http://ga4gh-schemas.readthedocs.io/en/latest/schemas/read_service.proto.html)

## NCBI APIs

The NCBI provides multiple ways to interrogate about data they provide.

### edirect

Returns XML metadata about projects, runs, and samples.

[Release announcement](https://www.ncbi.nlm.nih.gov/news/02-06-2014-entrez-direct-released/)

[Edirect Cookbook](https://github.com/NCBI-Hackathons/EDirectCookbook)


### NGS

Allows one to interrogate a run about aligned reads.

[Download link](https://github.com/ncbi/ngs/wiki/Downloads)

[Example usage](https://github.com/ncbi/ngs/tree/master/ngs-python/examples)
