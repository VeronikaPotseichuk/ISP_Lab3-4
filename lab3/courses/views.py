# from django.shortcuts import render
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from .mixins import OwnerCourseEditMixin, OwnerEditMixin, OwnerCourseMixin, OwnerMixin


import logging

logger = logging.getLogger(__name__)
message_ = '| user: %s | used: %s | method: %s'

'''
class CourseCreateView(OwnerCourseEditMixin,
                       OwnerEditMixin,
                       CreateView,
                       PermissionRequiredMixin):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin,
                       UpdateView,
                       PermissionRequiredMixin):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin,
                       DeleteView,
                       PermissionRequiredMixin):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'

'''