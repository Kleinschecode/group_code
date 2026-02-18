from mut import*

shift = mut(14,-1,11,2)
plane = mut(4,-1,8,1)
view = mut(11,-8,7,1)
lgiht = mut(14,-5,13,0,11,-7,7,1)
dp = mut(4,-1,8,1)

def mesh(*pts):
    frame = ap(mut(*pts,field=True),shift)
    print(f"==>> frame: {frame}")
    
  
mesh(0,0,0, 1,0,0, 0,1,0, 1,1,0, 1,0,-1, 1,1,-1, 0,0,-1, 0,1,-1)
