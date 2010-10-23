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
            if state.initial:
                states.append(state)
                ids.append(state.id)
                break
        if states:
            state = states[0]
            while state.next_id:
                if state.id not in ids:
                    states.append(state)
                    ids.append(state.id)
                state = state.next
        for state in self.states:
            if state.id not in ids:
                states.append(state)
                ids.append(state)
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
    initial = Bool()

def setup():
    WorkflowSet.states = ReferenceSet(WorkflowSet.id,
                                      WorkflowState.workflow_set_id)

    WorkflowState.set = Reference(WorkflowState.workflow_set_id,
                                  WorkflowSet.id)
    WorkflowState.next = Reference(WorkflowState.next_id, WorkflowState.id)
    WorkflowState.prev = Reference(WorkflowState.prev_id, WorkflowState.id)
