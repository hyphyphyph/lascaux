from lascaux.locals import Controller
from lascaux_app.model import store, LascauxApp


class LascauxController(Controller):
    def home(self):
        # writing data to a cookie is easy
        self.request.cookies['remember_my_name'] = True
        # let's save some things to session
        self.request.session['greeting'] = u'Hello World'
        self.request.session['byebye'] = u'Bye!'

    def new(self):
        if self.POST:
            print self.POST.get('name')
            return
        self.save(self.render('new'))

    def view(self, id):
        self.render()
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
