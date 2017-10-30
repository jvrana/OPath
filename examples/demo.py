from magicdir import MagicDir

env = MagicDir('bin')
s1 = env.add('core').add('session1')
s2 = env.core.add('session2')
t = env.session1.add('test')
env.mkdirs()
print(str(env.test.abspath))
# wait 1
assert t.abspath == env.test.abspath

env.print()
# wait 1
env.test.write('test.txt', 'w', 'Wow! This was easy!')

