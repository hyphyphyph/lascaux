from lascaux import Hook


class ProjectHook(Hook):

    def hook_braaains_project_view(self, project, blocks):
        issues = project.issues
        blocks["issue-list"] = self.render("issue-list", {"project": project,
                                                          "issues": issues})
