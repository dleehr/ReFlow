from operator import attrgetter
import io
import json

import fcm

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import \
    HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import inlineformset_factory

from guardian.shortcuts import assign_perm

from repository.models import *
from repository.forms import *


@login_required
def permission_denied(request):
    raise PermissionDenied


@login_required
def home(request):

    projects = Project.objects.get_projects_user_can_view(request.user)

    return render_to_response(
        'home.html',
        {
            'projects': sorted(projects, key=attrgetter('project_name')),
        },
        context_instance=RequestContext(request)
    )

#########################
### Non-project views ###
#########################


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def admin(request):
    return render_to_response(
        'admin.html',
        {},
        context_instance=RequestContext(request)
    )


@login_required
def view_specimens(request):

    specimens = Specimen.objects.all().values(
        'id',
        'specimen_name',
        'specimen_description',
    )

    return render_to_response(
        'view_specimens.html',
        {
            'specimens': specimens,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def add_specimen(request):
    if request.method == 'POST':
        form = SpecimenForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_specimens'))
    else:
        form = SpecimenForm()

    return render_to_response(
        'add_specimen.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def edit_specimen(request, specimen_id):
    specimen = get_object_or_404(Specimen, pk=specimen_id)

    if request.method == 'POST':
        form = SpecimenForm(request.POST, instance=specimen)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_specimens'))
    else:
        form = SpecimenForm(instance=specimen)

    return render_to_response(
        'edit_specimen.html',
        {
            'specimen': specimen,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_antibodies(request):

    antibodies = Antibody.objects.all().values(
        'id',
        'antibody_abbreviation',
        'antibody_name',
        'antibody_description',
    )

    return render_to_response(
        'view_antibodies.html',
        {
            'antibodies': antibodies,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def add_antibody(request):
    if request.method == 'POST':
        form = AntibodyForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_antibodies'))
    else:
        form = AntibodyForm()

    return render_to_response(
        'add_antibody.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def edit_antibody(request, antibody_id):
    antibody = get_object_or_404(Antibody, pk=antibody_id)

    if request.method == 'POST':
        form = AntibodyForm(request.POST, instance=antibody)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_antibodies'))
    else:
        form = AntibodyForm(instance=antibody)

    return render_to_response(
        'edit_antibody.html',
        {
            'antibody': antibody,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_fluorochromes(request):

    fluorochromes = Fluorochrome.objects.all().values(
        'id',
        'fluorochrome_abbreviation',
        'fluorochrome_name',
        'fluorochrome_description',
    )

    return render_to_response(
        'view_fluorochromes.html',
        {
            'fluorochromes': fluorochromes,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def add_fluorochrome(request):
    if request.method == 'POST':
        form = FluorochromeForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_fluorochromes'))
    else:
        form = FluorochromeForm()

    return render_to_response(
        'add_fluorochrome.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def edit_fluorochrome(request, fluorochrome_id):
    fluorochrome = get_object_or_404(Fluorochrome, pk=fluorochrome_id)

    if request.method == 'POST':
        form = FluorochromeForm(request.POST, instance=fluorochrome)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_fluorochromes'))
    else:
        form = FluorochromeForm(instance=fluorochrome)

    return render_to_response(
        'edit_fluorochrome.html',
        {
            'fluorochrome': fluorochrome,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


##############################
### Project specific views ###
##############################


@login_required
def view_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_sites = Site.objects.get_sites_user_can_view(
        request.user, project=project)

    if not project.has_view_permission(request.user) and not (
            user_sites.count() > 0):
                raise PermissionDenied

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)
    can_manage_project_users = project.has_user_management_permission(
        request.user)

    return render_to_response(
        'view_project.html',
        {
            'project': project,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
            'can_manage_project_users': can_manage_project_users,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(
    lambda user: user.is_superuser,
    login_url='/403',
    redirect_field_name=None)
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save()

            # Automatically add the request user to the project with all
            # permissions...it's the polite thing to do
            assign_perm('view_project_data', request.user, project)
            assign_perm('add_project_data', request.user, project)
            assign_perm('modify_project_data', request.user, project)
            assign_perm('manage_project_users', request.user, project)

            return HttpResponseRedirect(reverse(
                'view_project', args=(project.id,)))
    else:
        form = ProjectForm()

    return render_to_response(
        'add_project.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save()
            return HttpResponseRedirect(reverse(
                'view_project', args=(project.id,)))
    else:
        form = ProjectForm(instance=project)

    return render_to_response(
        'edit_project.html',
        {
            'project': project,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_project_users(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    can_manage_project_users = project.has_user_management_permission(
        request.user)

    if not can_manage_project_users:
        raise PermissionDenied

    project_users = project.get_project_users()

    return render_to_response(
        'view_project_users.html',
        {
            'project': project,
            'project_users': project_users,
            'can_manage_project_users': can_manage_project_users,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_user_permissions(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_user_management_permission(request.user):
        raise PermissionDenied

    form = UserSelectForm(request.POST or None, project_id=project_id)

    if request.method == 'POST' and form.is_valid():
        # is_valid calls clean so user should exist,
        # the id is now in cleaned_data
        if request.POST['site']:
            return HttpResponseRedirect(reverse(
                'manage_site_user',
                args=(request.POST['site'], form.cleaned_data['user'])))
        else:
            return HttpResponseRedirect(reverse(
                'manage_project_user',
                args=(project.id, form.cleaned_data['user'])))

    return render_to_response(
        'add_user_permissions.html',
        {
            'project': project,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def manage_project_user(request, project_id, user_id):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(User, pk=user_id)

    if not project.has_user_management_permission(request.user):
        raise PermissionDenied

    form = CustomUserObjectPermissionForm(user, project, request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save_obj_perms()
        return HttpResponseRedirect(reverse(
            'view_project_users', args=(project.id,)))

    return render_to_response(
        'manage_project_user.html',
        {
            'project': project,
            'project_user': user,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def manage_site_user(request, site_id, user_id):
    site = get_object_or_404(Site, pk=site_id)
    user = get_object_or_404(User, pk=user_id)

    if not site.project.has_user_management_permission(request.user):
        raise PermissionDenied
    if site.has_user_management_permission(request.user):
        raise PermissionDenied

    form = CustomUserObjectPermissionForm(user, site, request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save_obj_perms()
        return HttpResponseRedirect(reverse(
            'view_project_users', args=(site.project_id,)))

    return render_to_response(
        'manage_site_user.html',
        {
            'site': site,
            'site_user': user,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_project_stimulations(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_view_permission(request.user):
        raise PermissionDenied

    stimulations = Stimulation.objects.filter(project=project)

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)

    return render_to_response(
        'view_project_stimulations.html',
        {
            'project': project,
            'stimulations': stimulations,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_stimulation(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_add_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        stimulation = Stimulation(project=project)
        form = StimulationForm(request.POST, instance=stimulation)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse(
                'view_project_stimulations', args=(project_id,)))
    else:
        form = StimulationForm()

    return render_to_response(
        'add_project_stimulation.html',
        {
            'form': form,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_stimulation(request, stimulation_id):
    stimulation = get_object_or_404(Stimulation, pk=stimulation_id)

    if not stimulation.project.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = StimulationForm(request.POST, instance=stimulation)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_project_stimulations', args=(stimulation.project_id,)))
    else:
        form = StimulationForm(instance=stimulation)

    return render_to_response(
        'edit_project_stimulation.html',
        {
            'form': form,
            'stimulation': stimulation,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_project_panels(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    user_sites = Site.objects.get_sites_user_can_view(
        request.user,
        project=project)

    if not project.has_view_permission(request.user) and not (
            user_sites.count() > 0):
                raise PermissionDenied

    panels = ProjectPanel.objects.filter(project=project)

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)

    return render_to_response(
        'view_project_panels.html',
        {
            'project': project,
            'panels': panels,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_project_panel(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not (project.has_add_permission(request.user)):
        raise PermissionDenied

    if request.method == 'POST':
        panel_form = ProjectPanelForm(
            request.POST,
            instance=ProjectPanel(project=project),
            project_id=project.id)

        if panel_form.is_valid():
            panel = panel_form.save(commit=False)
            parameter_formset = ProjectParameterFormSet(
                request.POST,
                instance=panel)
            ab_formsets_valid = True

            for param_form in parameter_formset.forms:
                if param_form.nested:
                    if not param_form.nested[0].is_valid():
                        ab_formsets_valid = False

            if parameter_formset.is_valid() and ab_formsets_valid:
                panel.save()

                for param_form in parameter_formset.forms:
                    # when manually saving the forms in a formset the
                    # parent's id is not set
                    param_form.instance.project_panel_id = panel.id
                    parameter = param_form.save()
                    param_form.nested[0].instance = parameter
                    param_form.nested[0].save()

                return HttpResponseRedirect(reverse(
                    'view_project_panels',
                    args=(project.id,)))
        else:
            parameter_formset = ProjectParameterFormSet(
                request.POST,
                instance=ProjectPanel(project=project))

    else:
        panel = ProjectPanel(project=project)
        panel_form = ProjectPanelForm(
            instance=panel,
            project_id=project.id)
        parameter_formset = ProjectParameterFormSet(instance=panel)

    return render_to_response(
        'add_project_panel.html',
        {
            'panel_form': panel_form,
            'parameter_formset': parameter_formset,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_project_panel(request, panel_id):
    # TODO: make sure no site panels are based on this project panel

    # TODO: revamp this to allow full edits???
    panel = get_object_or_404(ProjectPanel, pk=panel_id)

    if not panel.project.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectPanelForm(
            request.POST,
            instance=panel,
            project_id=panel.project_id)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_project_panels',
                args=(panel.project_id,)))
    else:
        form = ProjectPanelForm(
            instance=panel,
            project_id=panel.project_id)

    return render_to_response(
        'edit_project_panel.html',
        {
            'form': form,
            'panel': panel,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_subjects(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    user_sites = Site.objects.get_sites_user_can_view(
        request.user,
        project=project)

    if not project.has_view_permission(request.user) and not (
            user_sites.count() > 0):
                raise PermissionDenied

    subjects = Subject.objects.filter(project=project).order_by('subject_code')

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)

    return render_to_response(
        'view_project_subjects.html',
        {
            'project': project,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
            'subjects': subjects,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_samples(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_view_sites = Site.objects.get_sites_user_can_view(
        request.user,
        project=project)

    # get user's sites based on their site_view_permission,
    # unless they have full project view permission
    if project.has_view_permission(request.user):
        samples = Sample.objects.filter(
            subject__project=project)
    elif user_view_sites.count() > 0:
        samples = Sample.objects.filter(
            subject__project=project,
            site__in=user_view_sites)
    else:
        raise PermissionDenied

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)
    user_add_sites = Site.objects.get_sites_user_can_add(
        request.user, project).values_list('id', flat=True)
    user_modify_sites = Site.objects.get_sites_user_can_modify(
        request.user, project).values_list('id', flat=True)

    return render_to_response(
        'view_project_samples.html',
        {
            'project': project,
            'samples': samples,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
            'user_add_sites': user_add_sites,
            'user_modify_sites': user_modify_sites
        },
        context_instance=RequestContext(request)
    )


@login_required
def render_sample_parameters(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)
    if not sample.has_view_permission(request.user):
        raise PermissionDenied

    return render_to_response(
        'render_sample_parameters.html',
        {
            'sample': sample
        },
        context_instance=RequestContext(request)
    )


@login_required
def render_sample_compensation(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)
    if not sample.has_view_permission(request.user):
        raise PermissionDenied

    return render_to_response(
        'render_sample_compensation.html',
        {
            'sample': sample
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_project_sites(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    sites = Site.objects.get_sites_user_can_view(request.user, project=project)

    if not (project.has_view_permission(request.user) or sites.count() > 0):
        raise PermissionDenied

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)

    return render_to_response(
        'view_project_sites.html',
        {
            'project': project,
            'sites': sites,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_site(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_add_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        site = Site(project=project)
        form = SiteForm(request.POST, instance=site)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse(
                'view_project_sites',
                args=(project_id,)))
    else:
        form = SiteForm()

    return render_to_response(
        'add_site.html',
        {
            'form': form,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_site(request, site_id):
    site = get_object_or_404(Site, pk=site_id)

    if not site.project.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_project_sites',
                args=(site.project_id,)))
    else:
        form = SiteForm(instance=site)

    return render_to_response(
        'edit_site.html',
        {
            'form': form,
            'site': site,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_project_site_panels(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_view_sites = Site.objects.get_sites_user_can_view(
        request.user,
        project=project)

    # get user's sites based on their site_view_permission,
    # unless they have full project view permission
    if project.has_view_permission(request.user):
        site_panels = SitePanel.objects.filter(
            site__project=project)
    elif user_view_sites.count() > 0:
        site_panels = Sample.objects.filter(
            site__project=project,
            site__in=user_view_sites)
    else:
        raise PermissionDenied

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)
    user_add_sites = Site.objects.get_sites_user_can_add(
        request.user, project).values_list('id', flat=True)
    user_modify_sites = Site.objects.get_sites_user_can_modify(
        request.user, project).values_list('id', flat=True)

    return render_to_response(
        'view_project_site_panels.html',
        {
            'project': project,
            'site_panels': site_panels,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
            'user_add_sites': user_add_sites,
            'user_modify_sites': user_modify_sites
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_compensations(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_view_sites = Site.objects.get_sites_user_can_view(
        request.user,
        project=project)

    if project.has_view_permission(request.user):
        compensations = Compensation.objects\
            .select_related()\
            .filter(site_panel__site__project=project)\
            .order_by('name')
    elif user_view_sites.count() > 0:
        compensations = Compensation.objects\
            .select_related()\
            .filter(site_panel__site__in=user_view_sites)\
            .order_by('name')
    else:
        raise PermissionDenied

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)
    user_add_sites = Site.objects.get_sites_user_can_add(
        request.user, project).values_list('id', flat=True)
    user_modify_sites = Site.objects.get_sites_user_can_modify(
        request.user, project).values_list('id', flat=True)

    return render_to_response(
        'view_project_compensations.html',
        {
            'project': project,
            'compensations': compensations,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
            'user_add_sites': user_add_sites,
            'user_modify_sites': user_modify_sites
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_compensation(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    user_sites = Site.objects.get_sites_user_can_add(request.user, project)

    if not (project.has_add_permission(request.user) or user_sites.count() > 0):
        raise PermissionDenied

    if request.method == 'POST':
        form = CompensationForm(
            request.POST,
            project_id=project_id,
            request=request)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'project_compensations',
                args=(project_id,)))
    else:
        form = CompensationForm(project_id=project_id, request=request)

    return render_to_response(
        'add_compensation.html',
        {
            'form': form,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_visit_types(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_sites = Site.objects.get_sites_user_can_view(
        request.user,
        project=project)

    if not project.has_view_permission(request.user) and not (
            user_sites.count() > 0):
                raise PermissionDenied

    visit_types = VisitType.objects.filter(
        project=project).order_by('visit_type_name')

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)

    return render_to_response(
        'view_project_visit_types.html',
        {
            'project': project,
            'visit_types': visit_types,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_visit_type(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_add_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        visit_type = VisitType(project=project)
        form = VisitTypeForm(request.POST, instance=visit_type)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'project_visit_types',
                args=(project_id,)))
    else:
        form = VisitTypeForm()

    return render_to_response(
        'add_visit_type.html',
        {
            'form': form,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_visit_type(request, visit_type_id):
    visit_type = get_object_or_404(VisitType, pk=visit_type_id)

    if not visit_type.project.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = VisitTypeForm(request.POST, instance=visit_type)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'project_visit_types',
                args=(visit_type.project_id,)))
    else:
        form = VisitTypeForm(instance=visit_type)

    return render_to_response(
        'edit_visit_type.html',
        {
            'form': form,
            'visit_type': visit_type,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_project_site_panel(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    preform_valid = False
    channels = {}
    project_panel = None
    site_panel_form = None
    parameter_formset = None

    user_sites = Site.objects.get_sites_user_can_add(request.user, project)

    if not (project.has_add_permission(request.user) or user_sites.count() > 0):
        raise PermissionDenied

    if request.method == 'POST':
        preform = PreSitePanelForm(
            request.POST,
            request.FILES,
            project_id=project_id,
            request=request)

        if preform.is_valid():
            preform_valid = True

            project_panel = preform.cleaned_data['project_panel']

            # process the FCS file
            fcm_obj = fcm.loadFCS(io.BytesIO(preform.files['fcs_file'].read()))
            sample_text_segment = fcm_obj.notes.text

            for key in sample_text_segment:
                matches = re.search('^P(\d+)([N,S])$', key, flags=re.IGNORECASE)
                if matches:
                    channel_number = int(matches.group(1))
                    n_or_s = str.lower(matches.group(2))
                    if channel_number not in channels:
                        channels[channel_number] = {}
                    channels[channel_number][n_or_s] = sample_text_segment[key]

            site_panel = preform.save(commit=False)
            site_panel_form = SitePanelForm(instance=site_panel)

            initial_param_data = list()
            for key in channels.keys():
                if 'n' in channels[key]:
                    n_text = channels[key]['n']
                else:
                    n_text = ""

                if 's' in channels[key]:
                    s_text = channels[key]['s']
                else:
                    s_text = ""

                initial_param_data.append({
                    'fcs_number': key,
                    'fcs_text': n_text,
                    'fcs_opt_text': s_text
                })

            ParameterFormSet = inlineformset_factory(
                SitePanel,
                SitePanelParameter,
                formset=BaseSitePanelParameterFormSet,
                extra=len(channels),
                can_delete=False,
                max_num=len(channels)
            )

            parameter_formset = ParameterFormSet(
                instance=site_panel,
                initial=initial_param_data)

            # Note that the formset POST will be handled in a different view.
            # (see the template formset action URL)
            # It would be a bit messy to differentiate an invalid pre-form
            # from the valid panel form.
        else:
            # If we get here the pre-form was invalid
            pass
    else:
        preform = PreSitePanelForm(
            project_id=project_id,
            request=request)

    return render_to_response(
        'add_project_site_panel.html',
        {
            'preform': preform,
            'preform_valid': preform_valid,
            'project': project,
            'project_panel': project_panel,
            'site_panel_form': site_panel_form,
            'parameter_formset': parameter_formset
        },
        context_instance=RequestContext(request)
    )


@login_required
def process_site_panel_post(request, project_id):
    if request.is_ajax():
        site_id = None
        if request.POST:
            if 'site' in request.POST:
                site_id = request.POST['site']

        if not site_id:
            return HttpResponseBadRequest()

        site = get_object_or_404(Site, pk=site_id)

        if not site.has_add_permission(request.user):
            raise PermissionDenied

        form = SitePanelForm(request.POST)

        if form.is_valid():
            if not 'sitepanelparameter_set-TOTAL_FORMS' in request.POST:
                return HttpResponseBadRequest()

            site_panel = form.save(commit=False)

            ParameterFormSet = inlineformset_factory(
                SitePanel,
                SitePanelParameter,
                formset=BaseSitePanelParameterFormSet,
                extra=11,
                can_delete=False
            )

            parameter_formset = ParameterFormSet(
                request.POST,
                instance=site_panel)

            if parameter_formset.is_valid():
                site_panel.save()

                for param_form in parameter_formset.forms:
                    # when manually saving the forms in a formset the
                    # parent's id is not set
                    param_form.instance.site_panel_id = site_panel.id
                    parameter = param_form.save()
                    param_form.nested[0].instance = parameter
                    param_form.nested[0].save()

                response_dict = {
                    'errors': False,
                    'messages': ["Thanks!"]
                }
                return HttpResponse(json.dumps(response_dict))
            else:
                response_dict = {
                    'errors': True,
                    'messages': []
                }
                for error in parameter_formset.non_form_errors():
                    response_dict['messages'].append(error)
                # for error in parameter_formset.errors:
                #     if error.has_key('__all__'):
                #         response_dict['messages'].append(error['__all__'])
                return HttpResponseBadRequest(json.dumps(response_dict))
        else:
            # If we get here the pre-form was invalid
            response_dict = {
                'errors': True,
                'messages': []
            }
            for error in form.non_field_errors():
                response_dict['messages'].append(error)
            return HttpResponseBadRequest(json.dumps(response_dict))

    return HttpResponseBadRequest()


@login_required
def edit_site_panel_parameters(request, panel_id):
    site_panel = get_object_or_404(SitePanel, pk=panel_id)
    project = site_panel.project_panel.project

    if not (site_panel.site.has_modify_permission(request.user)):
        raise PermissionDenied

    ParameterFormSet = inlineformset_factory(
        SitePanel,
        SitePanelParameter,
        formset=BaseSitePanelParameterFormSet,
        can_delete=False,
        extra=0
    )

    if request.method == 'POST':
        parameter_formset = ParameterFormSet(
            request.POST,
            instance=site_panel)

        if parameter_formset.is_valid():
            for param_form in parameter_formset.forms:
                # when manually saving the forms in a formset the
                # parent's id is not set
                param_form.instance.site_panel_id = site_panel.id
                parameter = param_form.save()
                param_form.nested[0].instance = parameter
                param_form.nested[0].save()

            response_dict = {
                'errors': False,
                'messages': ["Thanks!"]
            }
            return HttpResponse(json.dumps(response_dict))
        else:
            response_dict = {
                'errors': True,
                'messages': []
            }
            for error in parameter_formset.non_form_errors():
                response_dict['messages'].append(error)
            for error in parameter_formset.errors:
                 if error.has_key('__all__'):
                     response_dict['messages'].append(error['__all__'])
            return HttpResponseBadRequest(json.dumps(response_dict))
    else:
        parameter_formset = ParameterFormSet(instance=site_panel)

    return render_to_response(
        'edit_site_panel_parameters.html',
        {
            'project': project,
            'site_panel': site_panel,
            'parameter_formset': parameter_formset
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_site_panel_comments(request, panel_id):
    panel = get_object_or_404(SitePanel, pk=panel_id)

    if not panel.site.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = EditSitePanelForm(request.POST, instance=panel)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_project_site_panels',
                args=(panel.project_panel.project_id,)))
    else:
        form = EditSitePanelForm(instance=panel)

    return render_to_response(
        'edit_site_panel.html',
        {
            'form': form,
            'panel': panel,
        },
        context_instance=RequestContext(request)
    )


@login_required
def remove_panel_parameter(request, panel_parameter_id):
    ppm = get_object_or_404(SitePanelParameter, pk=panel_parameter_id)

    if not ppm.site_panel.site.has_modify_permission(request.user):
        raise PermissionDenied

    project = ppm.site_panel.site.project
    ppm.delete()

    return HttpResponseRedirect(reverse('project_panels', args=(project.id,)))


@login_required
def view_subject_groups(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_sites = Site.objects.get_sites_user_can_view(
        request.user,
        project=project)

    if not project.has_view_permission(request.user) and not (
            user_sites.count() > 0):
                raise PermissionDenied

    subject_groups = SubjectGroup.objects.filter(
        project=project).order_by('group_name')

    can_add_project_data = project.has_add_permission(request.user)
    can_modify_project_data = project.has_modify_permission(request.user)

    return render_to_response(
        'view_subject_groups.html',
        {
            'project': project,
            'subject_groups': subject_groups,
            'can_add_project_data': can_add_project_data,
            'can_modify_project_data': can_modify_project_data,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_subject_group(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_add_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        subject_group = SubjectGroup(project=project)
        form = SubjectGroupForm(request.POST, instance=subject_group)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'subject_groups',
                args=(project_id,)))
    else:
        form = SubjectGroupForm()

    return render_to_response(
        'add_subject_group.html',
        {
            'form': form,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_subject_group(request, project_id, subject_group_id):
    subject_group = get_object_or_404(
        SubjectGroup,
        pk=subject_group_id,
        project_id=project_id)

    if not subject_group.project.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = SubjectGroupForm(request.POST, instance=subject_group)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'subject_groups',
                args=(subject_group.project_id,)))
    else:
        form = SubjectGroupForm(instance=subject_group)

    return render_to_response(
        'edit_subject_group.html',
        {
            'form': form,
            'subject_group': subject_group,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_subject(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not project.has_add_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        subject = Subject(project=project)
        form = SubjectForm(
            request.POST,
            instance=subject,
            project_id=project_id)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_subjects',
                args=(project_id,)))

    else:
        form = SubjectForm(project_id=project_id)

    return render_to_response(
        'add_subject.html',
        {
            'form': form,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)

    if not subject.project.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = SubjectForm(
            request.POST,
            instance=subject,
            project_id=subject.subject_group.project_id)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_subjects',
                args=(subject.subject_group.project_id,)))
    else:
        form = SubjectForm(instance=subject, project_id=subject.project_id)

    return render_to_response(
        'edit_subject.html',
        {
            'form': form,
            'subject': subject,
        },
        context_instance=RequestContext(request)
    )


@login_required
def add_sample(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_sites = Site.objects.get_sites_user_can_add(request.user, project)

    if not (project.has_add_permission(request.user) or user_sites.count() > 0):
        raise PermissionDenied

    if request.method == 'POST':
        form = SampleForm(
            request.POST,
            request.FILES,
            project_id=project_id,
            request=request)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_project_samples',
                args=(project_id,)))
    else:
        form = SampleForm(project_id=project_id, request=request)

    return render_to_response(
        'add_sample.html',
        {
            'form': form,
            'project': project,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_sample(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)

    if not sample.site_panel.site.has_modify_permission(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = SampleEditForm(
            request.POST,
            request.FILES,
            instance=sample,
            request=request)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'view_project_samples',
                args=(sample.visit.project_id,)))
    else:
        form = SampleEditForm(
            instance=sample,
            project_id=sample.subject.project_id,
            request=request)

    return render_to_response(
        'edit_sample.html',
        {
            'form': form,
            'sample': sample,
        },
        context_instance=RequestContext(request)
    )


@login_required
def retrieve_sample(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)

    if not sample.site_panel.site.has_view_permission(request.user):
        raise PermissionDenied

    response = HttpResponse(
        sample.sample_file,
        content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % \
                                      sample.original_filename
    return response


@login_required
def retrieve_subsample(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)

    if not sample.site_panel.site.has_view_permission(request.user):
        raise PermissionDenied

    response = HttpResponse(
        sample.get_subsample_as_csv(),
        content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % \
                                      str(sample.id) + ".csv"
    return response


@login_required
def retrieve_compensation(request, compensation_id):
    compensation = get_object_or_404(Compensation, pk=compensation_id)

    if not compensation.site_panel.site.has_view_permission(request.user):
        raise PermissionDenied

    response = HttpResponse(
        compensation.get_compensation_as_csv(),
        content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % \
                                      "comp_" + str(compensation.id) + ".csv"
    return response


@login_required
def process_dashboard(request):

    plot_process = get_object_or_404(Process, process_name="Plot")
    workers = Worker.objects.all()
    requests = ProcessRequest.objects.filter(
        sample_set__project__in=Project.objects.get_projects_user_can_view(
            request.user))

    return render_to_response(
        'process_dashboard.html',
        {
            'plot_process': plot_process,
            'workers': sorted(workers, key=attrgetter('worker_name')),
            'requests': requests,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_process(request, process_id):
    process = get_object_or_404(Process, id=process_id)

    return render_to_response(
        'view_process.html',
        {
            'process': process,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def add_process_input(request, process_id):
    process = get_object_or_404(Process, pk=process_id)

    if request.method == 'POST':
        process_input = ProcessInput(process=process)
        form = ProcessInputForm(request.POST, instance=process_input)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse(
                'view_process',
                args=(process_id,)))
    else:
        form = ProcessInputForm()

    return render_to_response(
        'add_process_input.html',
        {
            'process': process,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def edit_process_input(request, process_input_id):
    process_input = get_object_or_404(ProcessInput, pk=process_input_id)

    if request.method == 'POST':
        form = ProcessInputForm(request.POST, instance=process_input)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse(
                'view_process',
                args=(process_input.process_id,)))
    else:
        form = ProcessInputForm(instance=process_input)

    return render_to_response(
        'edit_process_input.html',
        {
            'process_input': process_input,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def add_worker(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)

        if form.is_valid():
            worker = form.save()

            return HttpResponseRedirect(reverse(
                'view_worker',
                args=(worker.id,)))
    else:
        form = WorkerForm()

    return render_to_response(
        'add_worker.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def process_request_plot(request):
    process = get_object_or_404(Process, process_name='Plot')
    process_request = ProcessRequest(
        process=process,
        request_user=request.user)

    PRInputValueFormSet = inlineformset_factory(
        ProcessRequest,
        ProcessRequestInputValue,
        form=ProcessRequestInputValueForm,
        extra=process.processinput_set.count(),
        can_delete=False,
    )

    if request.method == 'POST':
        form = ProcessRequestForm(request.POST, instance=process_request)

        if form.is_valid():
            valid_request = form.save(commit=False)
            formset = PRInputValueFormSet(request.POST, instance=valid_request)

            if formset.is_valid():
                valid_request.save()
                formset.save()

                return HttpResponseRedirect(reverse('process_dashboard'))
        else:
            formset = PRInputValueFormSet(
                request.POST,
                instance=process_request)
    else:
        form = ProcessRequestForm(instance=process_request)

        initial_data = list()

        for process_input in process.processinput_set.all():
            # note that 'value_label' is
            # used for the 'value' field's label
            initial_data.append(
                {
                    'process_input': process_input,
                    'value_label': process_input.input_name
                })

        formset = PRInputValueFormSet(
            instance=process_request,
            initial=initial_data)

    return render_to_response(
        'process_request_plot.html',
        {
            'process': process,
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


@login_required
def view_process_request(request, process_request_id):
    process_request = get_object_or_404(ProcessRequest, pk=process_request_id)

    return render_to_response(
        'view_process_request.html',
        {
            'process_request': process_request,
        },
        context_instance=RequestContext(request)
    )