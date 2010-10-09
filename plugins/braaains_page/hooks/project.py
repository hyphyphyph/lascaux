from lascaux import Hook


class ProjectHook(Hook):

    def hook_braaains_project_view(self, project, blocks):
        blocks["page-list"] = u"Hello World"
