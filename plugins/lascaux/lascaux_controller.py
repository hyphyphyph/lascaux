from lascaux import Controller


class LascauxController(Controller):
    def view(self, id):
        self.save("HERE I AM, VIEWING HERE I AM, VIEWING HERE I AM, VIEWING %s" % id)
        self.save("""
            <form method="post" enctype="multipart/form-data" action="/lascaux/view/1">
                <div>
                    <input type="text" name="name" />
                    <input type="file" name="pic" />
                    <input type="submit" />
                </div>
            </form>
        """)
