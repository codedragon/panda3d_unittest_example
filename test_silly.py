import unittest
from panda3d.core import loadPrcFileData
from panda3d.core import Point3
from silly import SillyWorld
from direct.task.TaskManagerGlobal import taskMgr


class TestSillyWorld(unittest.TestCase):
    """ Test the SillyWorld class from silly.py. Some of these tests are probably overkill, 
    but I wanted to demonstrate different things you can test this way."""
    
    @classmethod
    def setUpClass(cls):
        loadPrcFileData("", "window-type offscreen")
        cls.w = SillyWorld()

    def setUp(self):
        """ 
        First issue is that we can't guarantee the order tests are run, so how do 
        we know we are at the beginning? Have a function in our SillyWorld class 
        that sets the models to the desired starting position and call this (is 
        also called from __init__, of course). This ensures we can always get
        back to the starting positions without creating a new ShowBase instance, 
        which would be bad. 
        """
        self.w.set_initial_positions()

    def test_smiley_shows_up(self):
        """ make sure smiley is rendered"""
        self.assertEqual(self.w.smiley.getParent(), base.render)
        
    def test_smiley_rendered_correct_position(self):
        """ make sure smiley is in correct position"""
        self.assertTrue(self.w.smiley.getPos(), Point3(0, 25, 0))
        
    def test_frowney_shows_up(self):
        """ make sure frowney is rendered to camera"""
        self.assertEqual(self.w.frowney.getParent(), base.camera)
        
    def test_frowney_rendered_correct_position(self):
        """ make sure frowney is in correct position"""
        self.assertTrue(self.w.frowney.getPos(), Point3(5, 25, 0))
        
    def test_frowney_disappears_when_collided_into(self):
        """ collide smiley into frowney, and make sure frowney goes away"""
        self.w.smiley.setPos(5, 25, 0)
        # Since we never ran run(), the game has not actually started yet, but
        # run() is just an infinite loop that runs Task.step() repeatedly, so
        # we can use taskMgr.step() to do this manually.
        # step through a couple of times to make sure collided    
        taskMgr.step()
        taskMgr.step()
        self.assertTrue(self.w.frowney.isStashed()) 
        # another idea is using a CollisionHandler in your code; you could put the
        # taskMgr.step() in a loop until you saw a collision that interested you, 
        # and then check that the behavior you expected occured after the collision.

    @classmethod
    def tearDownClass(cls):
        del cls.w

if __name__ == "__main__":
    unittest.main(verbosity=2)




