from django.contrib.auth.models import Group

def	extras(request):
	group = None
	groups = Group.objects.all()
	if request.user.groups.exists():
		group = request.user.groups.all()[0].name
	return {'group' : group}