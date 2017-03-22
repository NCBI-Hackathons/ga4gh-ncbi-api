# -*- coding: utf-8 -*-

from flask import Flask, json, request, render_template, Response, send_from_directory
from ga4gh.schemas import protocol

import ncbi


app = Flask(__name__, static_url_path='')


def _serialize_response(response_proto):
    return Response(
        protocol.toJson(response_proto), mimetype='application/json')

@app.route('/')
def index():
	return render_template('index.html', request=request)

def search_datasets(request):
    """
    Mock Function
    """
    dataset_list = []
    for i in xrange(10):
        dataset = protocol.Dataset()
        dataset.id = str(i)
        dataset.name = "Hi there"
        dataset_list.append(dataset)
    return (dataset_list, "0:0")

def search_read_group_sets(request):
    """
    Mock function
    """
    read_group_set_list = []
    for i in xrange(10):
        read_group_set = protocol.ReadGroupSet()
        read_group_set.id = str(i)
        read_group_set.name = "Hi there"
        read_group_set_list.append(read_group_set)
    return (read_group_set_list, "somepagetoken")

def search_reads(request):
    """
    Mock function
    """
    alignments = []
    for i in xrange(10):
        ga_alignment = protocol.ReadAlignment()
        ga_alignment.id = str(i)
        ga_alignment.alignment.position.position = 123 + i
        alignments.append(ga_alignment)
    return (alignments, "tokentoken")

@app.route('/datasets/search', methods=['POST'])
def search_datasets_route():
    search_request = protocol.SearchDatasetsRequest
    try:
    	deserialized_request = protocol.fromJson(request.get_data(), search_request)
    except Exception, e:
    	print str(e)
    dataset_list = ncbi.search_datasets(deserialized_request)
    response_proto = protocol.SearchDatasetsResponse()
    response_proto.datasets.extend(dataset_list)
    return _serialize_response(response_proto)

@app.route('/readgroupsets/search', methods=['POST'])
def search_read_group_sets_route():
    search_request = protocol.SearchReadGroupSetsRequest
    try:
    	deserialized_request = protocol.fromJson(request.get_data(), search_request)
    except Exception, e:
    	print str(e)
    read_group_set_list = ncbi.search_read_group_sets(deserialized_request)
    response_proto = protocol.SearchReadGroupSetsResponse()
    response_proto.read_group_sets.extend(read_group_set_list)
    return _serialize_response(response_proto)

@app.route('/reads/search', methods=['POST'])
def search_reads_route():
    search_request = protocol.SearchReadsRequest
    try:
    	deserialized_request = protocol.fromJson(request.get_data(), search_request)
    except Exception, e:
    	print str(e)
    alignment_list = ncbi.search_reads(deserialized_request)
    response_proto = protocol.SearchReadsResponse()
    response_proto.alignments.extend(alignment_list)
    return _serialize_response(response_proto)

def run_server():
    app.run(debug=True)

def get_app():
    return app

if __name__ == '__main__':
    run_server()
