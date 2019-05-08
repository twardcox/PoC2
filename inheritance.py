# Simple inheritance

# class Base:
#     def hello(self):
#         print("hello")
        
#     def message(self, msg):
#         print( msg)
        
# class Sub(Base):
#     def message(self, msg):
#         print( "sub:", msg)
        
# obj = Sub()
# obj.hello()
# obj.message("what's going to happen?")

# baseobj = Base()
# baseobj.hello()
# baseobj.message("another message")


"""
Simple example of using inheritance.
"""

class Base:
    """
    Simple base class.
    """    
    def __init__(self, num):
        self._number = num

    def __str__(self):
        """
        Return human readable string.
        """
        return str(self._number)
        
class Sub(Base):
    """
    Simple sub class.
    """
    def __init__(self, num):
        Base.__init__(self, num)
    
obj = Sub(42)
print(obj)
