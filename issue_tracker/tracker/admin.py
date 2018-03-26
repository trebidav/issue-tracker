from django.contrib import admin
from .models import Category, Issue

def assign_to_me(modeladmin, request, queryset):
	queryset.update(assignee=request.user)
	for obj in queryset:
		obj.save() # dirty hack to call pre_save signal as queryset.update doesn't call it
assign_to_me.short_description = "Assign to me"

def start_progress(modeladmin, request, queryset):
	queryset.update(state = Issue.IN_PROGRESS)
	for obj in queryset:
		obj.save()
start_progress.short_description = "Start progress"

def mark_as_done(modeladmin, request, queryset):
	for obj in queryset:
		obj.state=Issue.DONE
		obj.save()
mark_as_done.short_description = "Done"

class IssueAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'author', 'assignee', 'date_created', 'date_finished', 'state']
	list_filter = ['state']
	ordering = ['-date_created']
	actions = [assign_to_me, start_progress, mark_as_done]

	def save_model(self, request, instance, form, change):
		instance = form.save(commit=False)
		if not change or not instance.author:
			instance.author = request.user
		instance.save()
		return instance

	def changelist_view(self, request, extra_context=None, *args, **kwargs):
		extra_context = extra_context or {}
		fastest = Issue.get_fastest()
		slowest = Issue.get_slowest()
		average = Issue.get_average()
		if fastest == None:
			extra_context = {}
			return super(IssueAdmin, self).changelist_view(request, extra_context=extra_context)

		extra_context['fastest'] = fastest
		extra_context['fastest_time'] = (fastest.date_finished - fastest.date_created).seconds
		extra_context['slowest'] = slowest
		extra_context['slowest_time'] = (slowest.date_finished - slowest.date_created).seconds
		extra_context['average_time'] = int(Issue.get_average())

		return super(IssueAdmin, self).changelist_view(request, extra_context=extra_context)


class CategoryAdmin(admin.ModelAdmin):
	pass



# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Issue,IssueAdmin)


