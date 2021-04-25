from django.shortcuts import render


# >>>>>>>>>>>>>>>>>> START PAGE <<<<<<<<<<<<<<<<<
def start(request):
	context ={}
	return render(request, 'photographer/start.html', context)


# >>>>>>>>>>>> portrety page <<<<<<<<<<
def portrait(request):
	context = {}
	return render (request, 'photographer/portrety.html', context)


# >>>>>>>>>>>>>>>>> okolicznosciowe page <<<<<<<<<<<<<<<<<
def events(request):
	context = {}
	return render(request, 'photographer/okolicznosciowe.html', context)


# >>>>>>>>>>>>>>>>> okolicznosciowe page <<<<<<<<<<<<<<<<<
def family(request):
	context = {}
	return render(request, 'photographer/rodzinne.html', context)


# >>>>>>>>>>>>>>>>> sensualne page <<<<<<<<<<<<<<<<<
def sensuous(request):
	context = {}
	return render(request, 'photographer/sensualne.html', context)


# >>>>>>>>>>>>>>>>> wiecej page <<<<<<<<<<<<<<<<<
def more(request):
	context = {}
	return render(request, 'photographer/wiecej.html', context)


# >>>>>>>>>>>>>>>>> kontakt page <<<<<<<<<<<<<<<<<
def contact(request):
	context = {}
	return render(request, 'photographer/kontakt.html', context)



###########################################
def wieczor(request):
	context = {}
	return render(request, 'photographer/wieczor.html', context)

def chrzest(request):
	context = {}
	return render(request, 'photographer/chrzest.html', context)

def slub(request):
	context = {}
	return render(request, 'photographer/slub.html', context)
