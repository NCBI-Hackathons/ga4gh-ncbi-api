from flask import Flask, json, request, render_template
from ga4gh.schemas import protocol

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')
	
	
@app.route('/datasets/search', methods = ['POST'])
def SearchDatasets(request):
	search_request = protocol.SearchDatasetsRequest
	deserialized_request = protocol.fromJson(request_schema)
#	SearchDatasetsRequest = json.loads(SearchDataSetsRequest)
	return dese
	
@app.route('/datasets/<dataset_id>', methods = ['GET'])
def GetDataset(request):
	return Dataset
	
if __name__ == '__main__':
	app.run(debug = True)