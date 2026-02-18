import pygame as pg
from obj import*

class Game:
    def __init__(self):
        pg.init()
        self.res = self.w, self.h = (1600, 900) #self.h_w, self.h_h = self.w // 2, self.h // 2
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()
        self.scene = [cube]
        
    def vtx(face):
        vtx3d = np.array([m.M2N(basis=[14,13,11,7]) for m in face]).T 
        vtx3d = ((vtx3d/vtx3d[-1])*np.array([-1,1,-1,1]).T)[:-1]
        vtx2d = vtx3d/vtx3d[-1]
        vtx2d = ((vtx2d[:-1]).T+np.array([7,4]))*100
        return vtx2d
    
    def draw(self):
        self.screen.fill(pg.Color('black'))
        for object in self.scene:
            p = object.projection #; dp = object.dp
            for i,f in enumerate(p):               
                if object.z[i] < 0: pass
                if i == 5:
                        # if object.uv_cache is None:
                        #      object.uv_cache = uv_map(f[0],f[1],f[-1],d=9)
                        #      object.uv_cache_diff = uv_map(df[0],df[1],df[-1],d=9)

                        # else: object.uv_cache += object.uv_cache_diff
                        #print(f[0])
                        uv = uv_map(f[0],f[1],f[-1],d=15) # f is projective_point
                        sub_p = uv[0] # projective_point (?,4)
                        shade_vtx = uv[1].flatten() # projective_point
                        #print(sub_p.shape,shade_vtx.shape,object.shading_vertex.shape)
                        color = object.shading(shade_vtx,i)
                        #for j,sub_f in enumerate(sub_p): pg.draw.polygon(self.screen, (0,150*((j+1)/sub_p.shape[0]),255), Game.vtx(sub_f))
                        for j,sub_f in enumerate(sub_p): pg.draw.polygon(self.screen, np.clip(color[j],min=0,max=255), Game.vtx(sub_f)) 
                        #for j,sub_f in enumerate(object.cache): pg.draw.polygon(self.screen, (0,150*((j+1)/object.cache.shape[0]),255), Game.vtx(sub_f))
                        
                else: pg.draw.polygon(self.screen, (0,0,0) , Game.vtx(f)) #(0,50*i,255)
                pg.draw.polygon(self.screen, pg.Color('orange'), Game.vtx(f),4)
        
    def control(self):
        key = pg.key.get_pressed()
        dx = 5
        dt = 5
        # if key[pg.K_LEFT]: self.object.vts2d -= np.array([dx,0])
        # if key[pg.K_RIGHT]: self.object.vts2d += np.array([dx,0])
        if key[pg.K_d]: self.scene[0].rt(-dx,9)
        if key[pg.K_a]: self.scene[0].rt(dx,9)
        if key[pg.K_q]: self.scene[0].rt(-dt,5)
        if key[pg.K_e]: self.scene[0].rt(dt,5)
        if key[pg.K_w]: self.scene[0].rt(-dt,6)
        if key[pg.K_s]: self.scene[0].rt(dt,6)

        # if key[pg.K_r]:
        #     self.scene[0].frame = self.scene[0].temp
        #     self.scene[0].face = self.scene[0].temp_face

    def run(self):
        while True:
            self.draw()
            self.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption("Running at "+str(int(self.clock.get_fps()))+" fps")
            pg.display.flip()
            self.clock.tick(60)

def main() -> None:
    Engine = Game()
    Engine.run()

main()

# import cProfile
# if __name__ == '__main__':
#     cProfile.run('main()')