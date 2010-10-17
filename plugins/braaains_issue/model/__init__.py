from storm.locals import *

from lascaux.model_setup import User, Project
from plugins.braaains_workflow.model import WorkflowSet, WorkflowState


class IssueType(object):

    __export_to_model__ = True
    __storm_table__ = "issue_type"

    id = Int(primary=True)
    name = Unicode()
    title = Unicode()
    desc = Unicode()
    project_id = Int()
    project = Reference(project_id, Project.id)
    workflow_set_id = Int()
    workflow_set = Reference(workflow_set_id, WorkflowSet.id)


class Issue(object):

    __export_to_model__ = True
    __storm_table__ = "issue"

    id = Int(primary=True)
    issue_type_id = Int()
    type = Reference(issue_type_id, IssueType.id)
    workflow_state_id = Int()
    state = Reference(workflow_state_id, WorkflowState.id)
    project_id = Int()
    project = Reference(project_id, Project.id)
    user_uuid = Unicode()
    user = Reference(user_uuid, User.uuid)
    title = Unicode()
    body = Unicode()
    created = Int()
    updated = Int()


def setup():
    Project.issue_types = ReferenceSet(Project.id, IssueType.project_id)
    Project.issues = ReferenceSet(Project.id, Issue.project_id)
