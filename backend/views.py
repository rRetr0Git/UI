from django.shortcuts import render
import json
from django.http import JsonResponse,HttpResponse

def __get_response_alert():
	with open("./frontend/static/testApi/alert.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_alert(request):
	return JsonResponse(
		__get_response_alert(), safe=False
	)

def __get_response_graph():
	with open("./frontend/static/testApi/graph.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_graph(request):
	return JsonResponse(
		__get_response_graph(),safe=False
	)

def __get_response_overview():
	with open("./frontend/static/testApi/overview.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_overview(request):
	return JsonResponse(
		__get_response_overview()
	)

def __get_response_pe():
	with open("./frontend/static/testApi/pe.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_pe(request):
	return JsonResponse(
		__get_response_pe(),safe=False
	)

def __get_response_pe_interface_stats():
	with open("./frontend/static/testApi/pe_interface_stats.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_pe_interface_stats(request):
	return JsonResponse(
		__get_response_pe_interface_stats(),safe=False
	)

def __get_response_te_1():
	with open("./frontend/static/testApi/te_1.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_te_1(request):
	func = request.path.split('/')[-1].split('=')[-1]
	return HttpResponse(
		"{func}({info})".format(func=func, info=__get_response_te_1())
	)

def __get_response_te_if_state():
	with open("./frontend/static/testApi/te_if_state.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_te_if_state(request):
	func = request.path.split('/')[-1].split('=')[-1]
	return HttpResponse(
		"{func}({info})".format(func=func, info=__get_response_te_if_state())
	)

def __get_response_tenant_te_traffic():
	with open("./frontend/static/testApi/tenant_te_traffic.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_tenant_te_traffic(request):
	func = request.path.split('/')[-1].split('=')[-1]
	return HttpResponse(
		"{func}({info})".format(func=func, info=__get_response_tenant_te_traffic())
	)

def __get_response_top_10_if():
	with open("./frontend/static/testApi/top_10_if.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_top_10_if(request):
	return JsonResponse(
		__get_response_top_10_if(),safe=False
	)

def __get_response_traffic():
	with open("./frontend/static/testApi/traffic.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_traffic(request):
	return JsonResponse(
		__get_response_traffic(),safe=False
	)
'''

def __get_response_traffic():
	with open("./frontend/static/testApi/traffic.json", 'r') as f:
		ret = json.load(f)
		return ret

def get_api_traffic(request):
	return JsonResponse(
		__get_response_traffic(),safe=False
	)


'''
