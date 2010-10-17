from lascaux import Hook


class ProjectHook(Hook):

    def hook_braaains_project_view(self, project, blocks):
        pages = project.pages
        blocks["page-list"] = self.render("page-list", {"project": project,
                                                        "pages": pages})
