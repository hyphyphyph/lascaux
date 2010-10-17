from storm.locals import *


class WorkflowSet(object):

    __export_to_model__ = True
    __storm_table__ = "workflow_set"

    id = Int(primary=True)
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
    set = Reference(workflow_set_id, WorkflowSet.id)
    name = Unicode()
    title = Unicode()
    desc = Unicode()
    next_id = Int()
    prev_id = Int()


WorkflowState.next = Reference(WorkflowState.next_id, WorkflowState.id)
WorkflowState.prev = Reference(WorkflowState.prev_id, WorkflowState.id)

WorkflowSet.states = ReferenceSet(WorkflowSet.id, WorkflowState.workflow_set_id)
