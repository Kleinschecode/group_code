from mut import*
from shading import uv_map

from functools import reduce
import operator


class mesh():
    shift = np.array(mut(14,-1,11,2)) 
    light = np.array(mut(14,-5,13,0,11,-7,7,1)) ; view = np.array(mut(11,-8,7,1))
    plane = np.array(mut(4,-1,8,1))

    dp = np.array(mut(4,-1,8,1))

    def __init__(self,*pts):
        self.frame = np.array([mut(14,-x,13,y,11,-z,7,1) for (x,y,z) in np.array([pts]).reshape(-1,3)],dtype=object)
        self.frame = mesh.shift + self.frame
        self.face = np.array([[4,6,7,5],[6,0,2,7],[1,4,5,3],[6,4,1,0],[2,3,5,7],[0,1,3,2]])

        self.center = reduce(operator.__add__,self.frame)
        self.projection = (mesh.plane^(mesh.view & self.frame))[self.face] # Point: (6,4)
        self.shading_vertex = reduce(operator.__add__,(self.frame[self.face]).T) # Point: (6,)
        self.normal = reduce(operator.__and__, (self.frame[self.face]).T[:-1])
        self.z = np.array([m.M2N(basis=[0])[0] for m in self.normal|mesh.plane])

        self.uv_cache = None
        self.uv_cache_diff = None
        self.dp = None

    def m0(input): 
        arr = mut.arrM2N(basis=[0])(input) 
        arr = np.clip(np.array([x[0] for x in arr ]),min=0)
        return arr
 
    def array_op(x:"mut",y:"mut",op,x_norm=None,y_norm=None):
        if x_norm is None: x_norm = x**2
        if y_norm is None: y_norm = y**2
        #print("xy",x.shape,y.shape,x_norm,y_norm,((x^y)**2))
        if op =="dot": # specular <=> 
            out = (x|y)/(np.sqrt(x_norm)*np.sqrt(y_norm))
            out = mesh.m0(out)
        if op =="weg":
            #print((x^y)**2,(x_norm*y_norm))
            out = ((x^y)**2)/(x_norm*y_norm)  #np.array([m.negsqrt() for m in ((x^y)**2)/(x_norm*y_norm)])
            out = np.sqrt(mesh.m0(out))

        #print("out",out)
        # arr = np.abs(mut.arrM2N(basis=[0])(out))
        # new_arr = np.array([x[0] for x in arr])
        #print(arr,new_arr,new_arr[0],type(new_arr[0]))
        return out
            
    def shading(self,shading_point=None,si=5):
        if shading_point is None: shading_point = self.shading_vertex

        self.view_ray = mesh.view & shading_point   # global line: (sv,)
        self.light_ray = shading_point & mesh.light # global line: (sv,)

        #print(self.normal[si:si+1],self.normal)
    
        self.reflect = self.normal[si:si+1]*self.view_ray*self.normal[si:si+1] # (sv,)
        #self.reflect = self.normal*self.view_ray*self.normal

        #print(shading_point.shape,self.view_ray.shape,self.light_ray.shape,self.reflect.shape)

        self.specular = mesh.array_op(x=self.reflect,y=self.light_ray,op="dot")
        self.diffuse = mesh.array_op(x=self.normal[si:si+1],y=self.light_ray,op="weg")
        #self.diffuse = mesh.array_op(x=self.normal,y=self.light_ray,op="weg")

        lc = (1,1,1)#(.85,.85,.85)
        oc = (.75,.25,.25)

        ambient = 0.1
        specular = (self.specular**32).reshape(-1,1)
        diffuse = self.diffuse.reshape(-1,1)

        color = (ambient+diffuse+specular*0.7)*lc*oc*(255,255,255)
        #color = (specular*0.9)*lc*oc*(255,255,255)
        #print(color)

        return color
    
        # self.depth = mesh.array_op(self.normal,self.view_ray,"weg")

    def rt(self,dx,num):
        f0 = self.frame
        f1 = self.frame << mut(num,dx*0.005)
        df = f1 - f0
        #s2 = self.frame >> mut(num,1) #print(s2)
        
        self.frame = f1

        self.shading_vertex <<= mut(num,dx*0.005)
        self.normal <<= mut(num,dx*0.005)

        test = mesh.plane^(mesh.view & mut(num,1))
        a = self.projection
        for iy, ix in np.ndindex(a.shape): print(a[iy, ix],"rt::",mut.ep2(t=0.05,g=test)(a[iy, ix]))
      
        #print("test0",mut.ep2(t=0.05,g=test)(self.projection))
        #self.rp = mut(,dx*0.005)
        #self.p2 = self.projection<<self.rp

        self.dp = (mesh.plane^(mesh.view & df))[self.face]
        print(self.projection[0])

        self.projection += self.dp
        c = self.projection
        #self.projection = (mesh.plane^(mesh.view & self.frame))[self.face]

        
        print("----")
        print(self.projection[0])
        #mesh.dp <<= mut(num,dx*0.005)
        self.z = np.array([m.M2N(basis=[0])[0] for m in self.normal|mesh.plane])
        #self.uv_cache <<= mut(num,dx*0.005)
        
cube = mesh(0,0,0, 1,0,0, 0,1,0, 1,1,0, 1,0,-1, 1,1,-1, 0,0,-1, 0,1,-1)
#cube.shading()
cube.rt(dx=10,num=5)