from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from panda3d.core import CollisionNode, CollisionSphere
from panda3d.core import VBase4


class SillyWorld(DirectObject):

    def __init__(self):
        # start Panda3d
        base = ShowBase()
        # CollisionTraverser instance must be attached to base,
        # and must be called cTrav
        base.cTrav = CollisionTraverser()
        self.cHand = CollisionHandlerEvent()
        self.cHand.addInPattern('into-%in')
        
        # load smiley, which we will control
        # notice this is a little trickery. If we parent everything except smiley
        # to the camera, and the player is controlling the camera, then everything 
        # stays fixed in the same place relative to the camera, and when the camera
        # moves, the player is given the illusion that he is moving smiley, rather than 
        # the camera and the rest of the scene.
        self.smiley = base.loader.loadModel('smiley')
        self.smiley.reparentTo(render)
        self.smiley.setName('Smiley')
        
        # Setup a collision solid for this model. Our initCollisionSphere method returns
        # the cNodepath and the string representing it. We will use the cNodepath for 
        # adding to the traverser, and the string to accept it for event handling.
        #sColl = self.initCollisionSphere(self.smiley)
        sColl = self.initCollisionSphere(self.smiley, True)
        print 'smiley', sColl[0]
        print 'smiley', sColl[1]

        # Add this object to the traverser.
        base.cTrav.addCollider(sColl[0], self.cHand)

        # load frowney
        self.frowney = base.loader.loadModel('frowney')
        self.frowney.setName('Frowney')
        self.frowney.reparentTo(camera)
        
        # Setup a collision solid for this model.
        fColl = self.initCollisionSphere(self.frowney, True)
        #print 'frowney', fColl[0]
        #print 'frowney', fColl[1]
        
        # Add this object to the traverser.
        base.cTrav.addCollider(fColl[0], self.cHand)

        # Accept the events sent by the collisions.
        # smiley is the object we are 'moving', so by convention
        # it is the from object.
        # If we instead put smiley as the into object here,
        # it would work fine, but then smiley would disappear
        # when we collided them.
        self.accept('into-' + fColl[1], self.collide)        

        # set the initial positions of smiley and frowney
        self.set_initial_positions()
        
    def set_initial_positions(self):
        self.smiley.setPos(0, 25, 0)
        self.frowney.setPos(5, 25, 0)

    def collide(self, collEntry):
        #print('collision')
        #print collEntry.getIntoNodePath().getParent()
        collEntry.getIntoNodePath().getParent().stash()
        #print self.frowney.isStashed()
        # if instead of making frowney disappear, you wanted to 
        # change some aspect of one or both colliding objects,
        # you could do soemthing like this:
        colliderFROM = collEntry.getFromNodePath().getParent()
        #colliderINTO = collEntry.getIntoNodePath().getParent()
        # Note that for it to work, you have to 
        # we now may change the aspect of the two colliding objects
        #colliderINTO.setColor(1,1,1,1)
        colliderFROM.setScale(1.5)

    def initCollisionSphere(self, obj, show=False):
        # Get the size of the object for the collision sphere.
        bounds = obj.getChild(0).getBounds()
        center = bounds.getCenter()
        # We are making our radius bigger than our object. It will look strange
        # if we don't show the collision sphere, because frowney will disappear 
        # before the objects appear to touch, but this shows you how you can 
        # change the sphere separately from the actual object. Of course, you 
        # can make it the same size as the object if you want.
        radius = bounds.getRadius() * 1.1
 
        # Create a collision sphere and name it something understandable.
        collSphereStr = 'CollisionHull' + "_" + obj.getName()
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere(center, radius))
 
        cNodepath = obj.attachNewNode(cNode)
        if show:
            cNodepath.show()
 
        # Return a tuple with the collision node and its corrsponding string so
        # that the bitmask can be set.
        return (cNodepath, collSphereStr)

if __name__ == "__main__":
    W = SillyWorld()
    run()        

        

