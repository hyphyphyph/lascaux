from storm.locals import *


class IssueType(object):

    __export_to_model__ = True
    __storm_table__ = "issue_type"

    id = Int(primary=True)
    name = Unicode()
    title = Unicode()
    desc = Unicode()
    project_id = Int()
    workflow_set_id = Int()


class Issue(object):

    __export_to_model__ = True
    __storm_table__ = "issue"

    id = Int(primary=True)
    issue_type_id = Int()
    type = Reference(issue_type_id, IssueType.id)
    workflow_state_id = Int()
    project_id = Int()
    user_uuid = Unicode()
    title = Unicode()
    body = Unicode()
    created = Int()
    updated = Int()


class IssueComment(object):

    __export_to_model__ = True
    __storm_table__ = "issue_comment"

    id = Int(primary=True)
    issue_id = Int()
    user_uuid = Unicode()
    title = Unicode()
    body = Unicode()
    created = Int()


def setup():
    from lascaux.model_setup import User, Project, WorkflowSet, WorkflowState

    IssueType.project = Reference(IssueType.project_id, Project.id)
    IssueType.workflow_set = Reference(IssueType.workflow_set_id,
                                       WorkflowSet.id)

    Issue.state = Reference(Issue.workflow_state_id, WorkflowState.id)
    Issue.project = Reference(Issue.project_id, Project.id)
    Issue.user = Reference(Issue.user_uuid, User.uuid)
    Issue.comments = ReferenceSet(Issue.id, IssueComment.issue_id)

    IssueComment.issue = Reference(IssueComment.issue_id, Issue.id)
    IssueComment.user = Reference(IssueComment.user_uuid, User.uuid)

    Project.issue_types = ReferenceSet(Project.id, IssueType.project_id)
    Project.issues = ReferenceSet(Project.id, Issue.project_id)
