from process_manager.models import *
from django.contrib import admin

admin.site.register(Process)
admin.site.register(ProcessInput)
admin.site.register(ProcessOutput)

admin.site.register(Worker)
admin.site.register(WorkerProcessMap)

admin.site.register(ProcessRequest)
admin.site.register(ProcessRequestInputValue)