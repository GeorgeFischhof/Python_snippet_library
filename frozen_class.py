class MyFrozen:
   _frozen = False
   def __init__(self, ...):
       ...
       self._frozen = True

   def __setattr__(self, attr, value):
       if getattr(self, "_frozen"):
            raise AttributeError("Trying to set attribute on a frozen instance")
       return super().__setattr__(attr, value) 
