from storm.locals import *


class WorkflowSet(object):

    __export_to_model__ = True
    __storm_table__ = "workflow_set"

    id = Int(primary=True)
    project_id = Int()
    title = Unicode()
    desc = Unicode()

    def get_states(self):
        ids = []
        states = []
        for state in self.states:
            if not state.prev:
                ids.append(state.id)
                states.append(state)
        state = states and states[0]
        while state and state.next and state.next is not state:
            state = state.next
            states.append(state)
            ids.append(state.id)
        for state in self.states:
            if state.id not in ids:
                states.append(state)
                ids.append(state.id)
        return states


class WorkflowState(object):

    __export_to_model__ = True
    __storm_table__ = "workflow_state"

    id = Int(primary=True)
    workflow_set_id = Int()
    name = Unicode()
    title = Unicode()
    desc = Unicode()
    next_id = Int()
    prev_id = Int()


def setup():
    from lascaux.model_setup import Project

    WorkflowSet.states = ReferenceSet(WorkflowSet.id,
                                      WorkflowState.workflow_set_id)

    WorkflowState.set = Reference(WorkflowState.workflow_set_id,
                                  WorkflowSet.id)
    WorkflowState.next = Reference(WorkflowState.next_id, WorkflowState.id)
    WorkflowState.prev = Reference(WorkflowState.prev_id, WorkflowState.id)

    Project.workflow_sets = ReferenceSet(Project.id, WorkflowSet.project_id)
