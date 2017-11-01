from magicdir import *


class Session(object):
    """ A pretend session. """
    session = "default_session"

    @classmethod
    def set(cls, name):
        cls.session = name
        print("Switching to session \"{}\"".format(name))


class Environment(MagicDir):

    def __init__(self):
        super().__init__('bin')
        self.add('main')
        self.add('.environ', attr='environments')
        self.environments.add_file('default_env.pkl', attr='env')
        self.set_dir(Path(__file__).parent.absolute())

    @property
    def session(self):
        """ session is a dynamic folder whose name depends on Session.session """
        return self.main.add(Session.session)

    def category(self, cat):
        """ category is a dynamic folder in the session folder
        we put push_up=False so that the attribute doesn't get pushed back to root, this way we avoid having to
        use a unique name for each session/category combination we create
        """
        return self.session.add(cat, attr=cat, push_up=False)

    @property
    def session_pkl(self):
        """ This is some file in the session folder """
        return self.session.add_file('log.txt', attr='code', push_up=False)

env = Environment()
print(env.session_pkl.abspath)
print()
Session.set("session1")
print()
print(env.session_pkl.abspath)
print(env.category("category1").abspath)
print(env.category("category2").abspath)
print()
Session.set("session2")
print()
print(env.session_pkl.abspath)
print(env.category("category1").abspath)
print(env.category("category2").abspath)
print()

env.print()