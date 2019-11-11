import requests
import json

def mutual_funds():
	URL = "https://mutual-fund-api.p.rapidapi.com/api/v1/latestNav/133857"
	PARAMS = {'x-rapidapi-host':'mutual-fund-api.p.rapidapi.com','x-rapidapi-key':'df72b6035emshc31bb1cf2644645p13ba6djsn5a2e6bb07b0d'}
	response = requests.get(url = URL, headers = PARAMS)
	json_data = response.json()

	loaded_json = json.dumps(json_data['meta']['fund_house'])
	unload_json = json.dumps(json_data['data']['nav'])
	print(loaded_json , unload_json)


	URL1 = "https://mutual-fund-api.p.rapidapi.com/api/v1/latestNav/102000"
	PARAMS1 = {'x-rapidapi-host':'mutual-fund-api.p.rapidapi.com','x-rapidapi-key':'df72b6035emshc31bb1cf2644645p13ba6djsn5a2e6bb07b0d'}
	response1 = requests.get(url = URL1, headers = PARAMS1)
	json_data1 = response1.json()

	loaded_json1 = json.dumps(json_data1['meta']['fund_house'])
	unload_json1 = json.dumps(json_data1['data']['nav'])
	print(loaded_json1 , unload_json1)


	URL2 = "https://mutual-fund-api.p.rapidapi.com/api/v1/latestNav/128953"
	PARAMS2 = {'x-rapidapi-host':'mutual-fund-api.p.rapidapi.com','x-rapidapi-key':'df72b6035emshc31bb1cf2644645p13ba6djsn5a2e6bb07b0d'}
	response2 = requests.get(url = URL2, headers = PARAMS2)
	json_data2 = response2.json()

	loaded_json2 = json.dumps(json_data2['meta']['fund_house'])
	unload_json2 = json.dumps(json_data2['data']['nav'])
	print(loaded_json2 , unload_json2)

	URL3 = "https://mutual-fund-api.p.rapidapi.com/api/v1/latestNav/140770"
	PARAMS3 = {'x-rapidapi-host':'mutual-fund-api.p.rapidapi.com','x-rapidapi-key':'df72b6035emshc31bb1cf2644645p13ba6djsn5a2e6bb07b0d'}
	response3 = requests.get(url = URL3, headers = PARAMS3)
	json_data3 = response3.json()

	loaded_json3 = json.dumps(json_data3['meta']['fund_house'])
	unload_json3 = json.dumps(json_data3['data']['nav'])
	print(loaded_json3 , unload_json3)
	return loaded_json3 , unload_json3