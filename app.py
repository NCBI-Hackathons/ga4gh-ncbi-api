from flask import Flask, json, request, render_template
from ga4gh.schemas import protocol

app = Flask(__name__)


#@app.route('/')
#def index():
#	return render_template('index.html')

def get_datasets(request):
	"""
	SearchDatasetsRequest
	"""
	dataset_list = []
	for i in xrange(10):
		dataset = protocol.Dataset()
		dataset.id = str(i)
		dataset.name = "Hi there"
		dataset_list.append(dataset)
	return dataset_list

@app.route('/datasets/search', methods=['POST'])
def Search_Datasets():
	search_request = protocol.SearchDatasetsRequest
	deserialized_request = protocol.fromJson(request.get_data(), search_request)
	dataset_list = get_datasets(deserialized_request)
	response_proto = protocol.SearchDatasetsResponse()
	response_proto.datasets.extend(dataset_list)
	return protocol.toJson(response_proto)


if __name__ == '__main__':
	app.run(debug = True)