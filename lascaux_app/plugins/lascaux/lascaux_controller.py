# from lascaux.model import User, create_store
from lascaux.locals import Controller


class LascauxController(Controller):
    def home(self):
        pass

    def view(self, id):
        pass
        # if self.POST:
        #     store = create_store()
        #     user = User()
        #     user.uuid = u"123"
        #     user.username = u"ABDEKHKHFDA"
        #     store.add(user)
        #     store.flush()
        #     self.save("HERE I AM, VIEWING HERE I AM, VIEWING HERE I AM, VIEWING %s" % id)
        # else:
        #     self.save("""
        #         <form method="post" enctype="multipart/form-data" action="/lascaux/view/1">
        #             <div>
        #                 <input type="text" name="name" />
        #                 <input type="file" name="pic" />
        #                 <input type="submit" />
        #             </div>
        #         </form>
        #     """)
