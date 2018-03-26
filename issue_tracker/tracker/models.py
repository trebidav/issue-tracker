from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
import datetime
import sys


def max_time(issues):
	max = 0
	ret = None
	for issue in issues:
		delta = (issue.date_finished - issue.date_created).seconds
		if delta > max:
			max = delta
			ret = issue
	return ret

def min_time(issues):
	min = sys.maxsize
	ret = None
	for issue in issues:
		delta = (issue.date_finished - issue.date_created).seconds
		if delta < min:
			min = delta
			ret = issue
	return ret

def avg_time(issues):
	sum = 0;
	for issue in issues:
		sum += (issue.date_finished - issue.date_created).seconds
	if len(issues):
		return sum/len(issues)
	else:
		return sum;


# Create your models here.
class Category(models.Model):
	class Meta:
		verbose_name_plural = "categories"
	name = models.CharField(max_length=64)
	description = models.TextField(max_length=300)
	def __str__(self):
		return self.name

class Issue(models.Model):
	
	UNASSIGNED 	= 'U'
	ASSIGNED 	= 'A'
	IN_PROGRESS	= 'P'
	DONE 		= 'D'
	
	STATES = (
		(UNASSIGNED, 	'Unassigned'),
		(ASSIGNED, 		'Assigned'),
		(IN_PROGRESS, 	'In progress'),
		(DONE, 			'Done'),
	)

	author 			= models.ForeignKey(User, on_delete=models.PROTECT, editable=False, related_name='%(class)s_issue_created')
	assignee 		= models.ForeignKey(User, unique=False, on_delete=models.PROTECT, editable=True, null=True, blank=True, default=None, related_name='%(class)s_issue_assigned')
	name 			= models.CharField(max_length=64)
	description 	= models.TextField(max_length=300)
	category 		= models.ForeignKey('Category', on_delete=models.PROTECT)
	date_created 	= models.DateTimeField(auto_now=False, auto_now_add=True)
	date_finished 	= models.DateTimeField(auto_now=False, auto_now_add=False, default=None, null=True, blank=True)
	state 			= models.CharField(max_length=1, choices=STATES, default=UNASSIGNED)

	def __str__(self):
		return "[%s] %s" % (self.category.name, self.name)

	def get_fastest():
		return min_time(Issue.objects.exclude(date_finished=None))

	def get_slowest():
		return max_time(Issue.objects.exclude(date_finished=None))

	def get_average():
		return avg_time(Issue.objects.exclude(date_finished=None))


@receiver(pre_save, sender=Issue)
def validate(sender, instance, **kwargs):
	if instance.assignee != None and instance.state == Issue.UNASSIGNED:
		instance.state = Issue.ASSIGNED
		instance.date_finished = None

	if instance.assignee == None:
		instance.state = Issue.UNASSIGNED
		instance.date_finished = None

	if instance.state == Issue.IN_PROGRESS or instance.state == Issue.ASSIGNED:
		instance.date_finished = None

	if instance.state == Issue.DONE:
		original = Issue.objects.get(pk=instance.pk)
		if instance.state != original.state:
			instance.date_finished = datetime.datetime.now()



