from lascaux.model import LafItem

from lascaux import Hook


class UserLoginRedirect(Hook):

    def hook_user_register(self, user, redirect):
        item_id = self.controller.session.get("last_created_item_id")
        if item_id:
            self.controller.session.unset("last_created_item_id")
        item = self.db.get(LafItem, item_id)
        if item:
            item.workflow_state_id = item.state.next.id
            r = self.controller.redirect("laf", "post_register",
                                         {"id": item_id})
            redirect["redirect"] = r
