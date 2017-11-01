"""
The following is an example of a dynamically generated environment using the Borg Idiom. The borg idiom is used such
that, whereever the Environment is initialize, it is gauranteed to have the same paths [i.e. Environment() is
functionally equivalent to a new Environment() instance]

This example is comprised of dynamically generated "session" folders located in the "bin/main" folder. When the session
changes, and the session property is called, a new folder is dynamically generated.

The category method generates a new folder in the current session folder by name.

The session_pkl dynamically creates a file path based on the current session. Sending env.code.write(...) will
automatically create the parent folders and the file.

Clicking run, you'll see a printed version of the current abstracted directory tree. In the example folder,
you'll find that only the dirs necessary for the writing of the log.txt file were created. To create all folders,
run the mkdirs() command.
"""



from magicdir import *

class Session(object):
    """ A pretend session. """
    session = "default_session"

    @classmethod
    def set(cls, name):
        cls.session = name
        print("Switching to session \"{}\"".format(name))


class Environment(MagicDir):
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state # Borg Idiom
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

env2 = Environment()
Session.set('sldjflkjdf')
assert env2.session == env.session