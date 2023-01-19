#Computer Science FSE
#The Great Escape
#By: Ahmad Munim

from pygame import *
from random import *
from math import *
init()

GRAVITY=0.7
power=11

#DEFINING VARIABLES
RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)

level_four_platforms=[Rect(150,758,1024-150,10),Rect(900,700,40,10),
                      Rect(970,620,40,10),Rect(900,540,40,10),
                      Rect(0,450,1024-150,10),Rect(0,380,30,10),
                      Rect(150,310,1024-50,10),Rect(982,240,60,10),
                      Rect(0,160,900,10)]

mypics=[]
X=0
Y=1
VY=2
ONGROUND=3
frame=0
move=0

starting_point=100
ending_point=500


#OBSTACLES
fireRects=[Rect(1000,90,70,70),Rect(1000,400,70,70),Rect(1000,245,70,70),Rect(1000,650,70,70)]
fireRects_lvl3=[Rect(1000,300,70,70),Rect(0,190,70,70)]
player_locations=[[200,768-31]]

enemies_lvl4=[Rect(400,450-31,18,31),Rect(600,450-31,18,31),Rect(700,450-31,18,31),Rect(300,450-31,18,31),
                      Rect(300,310-31,18,31),Rect(500,310-31,18,31),Rect(700,310-31,18,31),Rect(1000,310-31,18,31),
                      Rect(0,160-31,18,31),Rect(200,160-31,18,31),Rect(400,160-31,18,31),Rect(600,160-31,18,31),Rect(750,160-31,18,31)]

   #X  Y   VY   ONGROUND
guy=[starting_point,ending_point,0,True]#250 is the position in the "world"

initial_spikes=image.load("Spikes.png")
initial_platforms=image.load("platform_edited.png")
initial_boss=image.load("final_boss.png")

def addPics(name,start,end):

    mypics=[]
    for i in range(start,end+1):
        mypics.append(image.load("%s/%s%03d.png" %(name,name,i)))#adds picture to the list. Uses variables to define file name
    return mypics

pics=[addPics("Ninja",2,4),
      addPics("Ninja",7,9),
      addPics("Ninja",17,18)]
        
def moveGuy(guy):

    global move,frame,pics
    keys=key.get_pressed()
    newMove=-1#this variable checks which pictures to use in the given direction (right,left,jump) of players

    if keys[K_LEFT]:
        if not guy[X]<0:
            newMove=0
            guy[X]-=5#moves player left
    if keys[K_RIGHT]:
        if not guy[X]>1022:
            newMove=1
            guy[X]+=5#moves player right
    if keys[K_SPACE] and guy[ONGROUND]:#only if on ground
        newMove=2
        guy[VY] -= power
        guy[ONGROUND] = False#only when player is in the air so the player doesnt keep jumping

    if move==newMove:#checks which way the player is going to apply a specific frame
        frame=frame+0.2
        if frame>=len(pics[move]):
            frame=1
    elif newMove!=-1:
        move=newMove
        frame=1

    guy[Y] += guy[VY]#applies gravity

    if guy[Y]>=740:#the ground level
        guy[Y]=740#keep him on the ground
        guy[VY]=0
        guy[ONGROUND]= True

    guy[VY] += GRAVITY #applying gravity      

def fireballs():

    global fireRects,fireRects_lvl3
    
    for fireball in fireRects:
        fireball.left-=5#moves fireball to the left of the screen
        if fireball.right<=0:#when it leaves the screen
            fireball.left=1000#back to starting position

    if page=="level_three":
        fireRects_lvl3[0].left-=5
        if fireRects_lvl3[0].right<=0:
            fireRects_lvl3[0].left=1000

        fireRects_lvl3[1].right+=5
        if fireRects_lvl3[1].left>=1024:
            fireRects_lvl3[1].right=0

x=1
x_component=x-0
y_component=768-0
laser_x=int(0)
laser_y=int(0)

def lasers(y,player):

    global x,starting_point,ending_point,x_component,y_component,laser_x,laser_y

    rec=Rect(guy[X],guy[Y],18,31)

    for p in player:
        
        laser_x=int(0)
        laser_y=int(0)
        x+=1
        x_component+=1
        dist=sqrt(x_component**2+y_component**2)
        for d in range(10,int(dist),1):#sets up the drawing of circles on the laser line
            dotX=int(x_component*d/dist)
            dotY=int(y_component*d/dist)
            draw.circle(screen,RED,(dotX,dotY),1)
            if rec.collidepoint(dotX,dotY):#if you hit any of the drawn circles along the laser you die
                guy[X]=starting_point
                guy[Y]=ending_point
                x_component=1
            if rec.collidepoint(850,575-31):
                if guy[X]<850:
                    x=1
                    x_component=1
                    x+=1
                    x_component+=1 


    if guy[X]==starting_point:
        x=1
        x_component=1

def level_one():

    global pics,frame
    
    running = True
    myClock = time.Clock()
    while running:
        
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

        spikes=[Rect(0,748,1024,20)]
            
        level_one_platforms=[Rect(30,550,100,20),Rect(200,630,40,50),
                         Rect(300,680,100,50),Rect(500,610,60,50),
                         Rect(700,590,50,50),Rect(840,520,60,50),
                         Rect(720,450,60,50),Rect(540,390,60,50),
                         Rect(340,360,60,50),Rect(110,320,60,50),
                         Rect(300,260,60,50),Rect(415,190,60,50),
                         Rect(660,180,60,50),Rect(800,150,100,20)]

        screen.fill(BLACK)
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        rec=Rect(guy[X],guy[Y],18,31)
        keys=key.get_pressed()
        
        for i in range(len(spikes)):
            draw.rect(screen,BLACK,spikes[i])

        for i in range(len(level_one_platforms)):
            draw.rect(screen,BLACK,level_one_platforms[i])

        finalPlatform1=transform.scale(initial_platforms,(100,20))
        finalPlatform2=transform.scale(initial_platforms,(40,50))
        finalPlatform3=transform.scale(initial_platforms,(100,50))
        finalPlatform4=transform.scale(initial_platforms,(60,50))
        finalPlatform5=transform.scale(initial_platforms,(50,50))
        finalPlatform6=transform.scale(initial_platforms,(60,50))
        finalPlatform7=transform.scale(initial_platforms,(60,50))
        finalPlatform8=transform.scale(initial_platforms,(60,50))
        finalPlatform9=transform.scale(initial_platforms,(60,50))
        finalPlatform10=transform.scale(initial_platforms,(60,50))
        finalPlatform11=transform.scale(initial_platforms,(60,50))
        finalPlatform12=transform.scale(initial_platforms,(60,50))
        finalPlatform13=transform.scale(initial_platforms,(60,50))
        finalPlatform14=transform.scale(initial_platforms,(100,20))

        screen.blit(finalPlatform1,(30,550))
        screen.blit(finalPlatform2,(200,630))
        screen.blit(finalPlatform3,(300,680))
        screen.blit(finalPlatform4,(500,610))
        screen.blit(finalPlatform5,(700,590))
        screen.blit(finalPlatform6,(840,520))
        screen.blit(finalPlatform7,(720,450))
        screen.blit(finalPlatform8,(540,390))
        screen.blit(finalPlatform9,(340,360))
        screen.blit(finalPlatform10,(110,320))
        screen.blit(finalPlatform11,(300,260))
        screen.blit(finalPlatform12,(415,190))
        screen.blit(finalPlatform13,(660,180))
        screen.blit(finalPlatform14,(800,150))
        
        final_spikes=transform.scale(initial_spikes,(1024,20))
        screen.blit(final_spikes,(0,748))
        draw.rect(screen,BLACK,(guy[X],guy[Y],18,31))
        moveGuy(guy)
        checkCollision(guy,level_one_platforms,spikes)
        screen.blit(pics[move][int(frame)],(guy[X],guy[Y]))#blits the animated picture using move and frame variable

        if rec.collidepoint(800,150-31):#this is when the player completes the level
            guy[X]=30
            guy[Y]=545
            starting_point=35
            ending_point=545
            return "level_two"#calls next level

        
        myClock.tick(60)
        display.flip()
    return "menu"

def level_two():

    global fireRects
    
    running = True
    myClock = time.Clock()
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        
        spikes=[Rect(0,748,1024,20),Rect(190,630,70,20),
                Rect(170,470,10,90),Rect(420,445,80,10),
                Rect(520,290,80,10),Rect(100,290,180,10)]

        screen.fill(BLACK)
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()

        level_two_platforms=[Rect(30,580,100,20),Rect(140,680,100,20),
                             Rect(190,640,70,20),Rect(270,610,100,20),
                             Rect(550,600,100,20),Rect(180,470,10,90),
                             Rect(375,515,100,20),Rect(210,470,100,20),
                             Rect(50,450,100,20),Rect(300,380,100,20),
                             Rect(525,390,100,20),Rect(420,455,80,10),
                             Rect(705,370,100,20),Rect(900,300,100,20),
                             Rect(650,270,100,20),Rect(400,230,100,20),
                             Rect(300,150,100,20),Rect(520,300,80,10),
                             Rect(110,90,100,20),Rect(100,300,180,10)]

        for i in range(len(spikes)):
            draw.rect(screen,BLACK,spikes[i])

        for i in range(len(level_two_platforms)):
            draw.rect(screen,BLACK,level_two_platforms[i])

        finalPlatform1=transform.scale(initial_platforms,(100,20))
        finalPlatform2=transform.scale(initial_platforms,(100,20))
        finalPlatform3=transform.scale(initial_platforms,(70,20))
        finalPlatform4=transform.scale(initial_platforms,(100,20))
        finalPlatform5=transform.scale(initial_platforms,(100,20))
        finalPlatform6=transform.scale(initial_platforms,(10,90))
        finalPlatform7=transform.scale(initial_platforms,(100,20))
        finalPlatform8=transform.scale(initial_platforms,(100,20))
        finalPlatform9=transform.scale(initial_platforms,(100,20))
        finalPlatform10=transform.scale(initial_platforms,(100,20))
        finalPlatform11=transform.scale(initial_platforms,(100,20))
        finalPlatform12=transform.scale(initial_platforms,(80,10))
        finalPlatform13=transform.scale(initial_platforms,(60,50))
        finalPlatform14=transform.scale(initial_platforms,(100,20))
        finalPlatform15=transform.scale(initial_platforms,(100,20))
        finalPlatform16=transform.scale(initial_platforms,(100,20))
        finalPlatform17=transform.scale(initial_platforms,(100,20))
        finalPlatform18=transform.scale(initial_platforms,(80,10))
        finalPlatform19=transform.scale(initial_platforms,(100,20))
        finalPlatform20=transform.scale(initial_platforms,(180,10))

        screen.blit(finalPlatform1,(30,580))
        screen.blit(finalPlatform2,(140,680))
        screen.blit(finalPlatform3,(190,640))
        screen.blit(finalPlatform4,(270,610))
        screen.blit(finalPlatform5,(550,600))
        screen.blit(finalPlatform6,(180,470))
        screen.blit(finalPlatform7,(375,515))
        screen.blit(finalPlatform8,(210,470))
        screen.blit(finalPlatform9,(50,450))
        screen.blit(finalPlatform10,(300,380))
        screen.blit(finalPlatform11,(525,390))
        screen.blit(finalPlatform12,(420,455))
        screen.blit(finalPlatform13,(705,370))
        screen.blit(finalPlatform14,(900,300))
        screen.blit(finalPlatform15,(650,270))
        screen.blit(finalPlatform16,(400,230))
        screen.blit(finalPlatform17,(300,150))
        screen.blit(finalPlatform18,(520,300))
        screen.blit(finalPlatform19,(110,90))
        screen.blit(finalPlatform20,(100,300))

        final_spikes1=transform.scale(initial_spikes,(1024,20))
        final_spikes2=transform.scale(initial_spikes,(70,10))
        final_spikes3=transform.scale(initial_spikes,(90,10))
        final_spikes3=transform.rotate(final_spikes3,(90))
        final_spikes4=transform.scale(initial_spikes,(80,10))
        final_spikes5=transform.scale(initial_spikes,(80,10))
        final_spikes6=transform.scale(initial_spikes,(180,10))

        screen.blit(final_spikes1,(0,748))
        screen.blit(final_spikes2,(190,630))
        screen.blit(final_spikes3,(170,470))
        screen.blit(final_spikes4,(420,445))
        screen.blit(final_spikes5,(520,290))
        screen.blit(final_spikes6,(100,290))

        rec=Rect(guy[X],guy[Y],18,31)
        draw.rect(screen,BLACK,rec)
        moveGuy(guy)
        fireballs()
        checkCollision(guy,level_two_platforms,spikes)
        screen.blit(pics[move][int(frame)],(guy[X],guy[Y]))

        for fireball in fireRects:
            draw.rect(screen,(255,140,0),fireball)

        if rec.collidepoint(110,90-31):
            guy[X]=50
            guy[Y]=500
            starting_point=35
            ending_point=545
            return "level_three"
            
    
        myClock.tick(60)
        display.flip()
    return "menu"

def level_three():

    global x,fireRects_lvl3,laser_x,laser_y
    
    running = True
    myClock = time.Clock()
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        
        level_three_platforms=[Rect(400,700,100,10),Rect(651,650,100,10),
                               Rect(850,575,100,10),Rect(570,560,100,10),
                               Rect(400,555,100,10),Rect(120,550,100,10),
                               Rect(60,500,100,10),Rect(250,420,100,10),
                               Rect(520,405,100,10),Rect(800,395,100,10),
                               Rect(620,330,100,10),Rect(400,300,100,10),
                               Rect(200,310,100,10),Rect(280,620,100,10),
                               Rect(280,440,100,10),Rect(450,500,60,10),
                               Rect(430,425,70,10),Rect(660,470,100,10)]

        spikes=[Rect(500,758,524,10),Rect(450,500,50,10),Rect(280,610,100,10),
                Rect(280,450,100,10),Rect(430,415,70,10),Rect(660,460,100,10)]
        
        screen.fill(BLACK)
        rec=Rect(guy[X],guy[Y],18,31)
        draw.rect(screen,BLACK,rec)
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()

        for i in range(len(spikes)):
            draw.rect(screen,BLACK,spikes[i])

        for i in range(len(level_three_platforms)):
            draw.rect(screen,BLACK,level_three_platforms[i])

        finalPlatform1=transform.scale(initial_platforms,(100,10))
        finalPlatform2=transform.scale(initial_platforms,(100,10))
        finalPlatform3=transform.scale(initial_platforms,(100,10))
        finalPlatform4=transform.scale(initial_platforms,(100,10))
        finalPlatform5=transform.scale(initial_platforms,(100,10))
        finalPlatform6=transform.scale(initial_platforms,(100,10))
        finalPlatform7=transform.scale(initial_platforms,(100,10))
        finalPlatform8=transform.scale(initial_platforms,(100,10))
        finalPlatform9=transform.scale(initial_platforms,(100,10))
        finalPlatform10=transform.scale(initial_platforms,(100,10))
        finalPlatform11=transform.scale(initial_platforms,(100,10))
        finalPlatform12=transform.scale(initial_platforms,(100,10))
        finalPlatform13=transform.scale(initial_platforms,(100,10))
        finalPlatform14=transform.scale(initial_platforms,(100,10))
        finalPlatform15=transform.scale(initial_platforms,(100,10))
        finalPlatform16=transform.scale(initial_platforms,(60,10))
        finalPlatform17=transform.scale(initial_platforms,(70,10))
        finalPlatform18=transform.scale(initial_platforms,(100,10))

        screen.blit(finalPlatform1,(400,700))
        screen.blit(finalPlatform2,(651,650))
        screen.blit(finalPlatform3,(850,575))
        screen.blit(finalPlatform4,(570,560))
        screen.blit(finalPlatform5,(400,555))
        screen.blit(finalPlatform6,(120,550))
        screen.blit(finalPlatform7,(60,500))
        screen.blit(finalPlatform8,(250,420))
        screen.blit(finalPlatform9,(520,405))
        screen.blit(finalPlatform10,(800,395))
        screen.blit(finalPlatform11,(620,330))
        screen.blit(finalPlatform12,(400,300))
        screen.blit(finalPlatform13,(200,310))
        screen.blit(finalPlatform14,(280,620))
        screen.blit(finalPlatform15,(280,440))
        screen.blit(finalPlatform16,(450,510))
        screen.blit(finalPlatform17,(430,425))
        screen.blit(finalPlatform18,(660,460))
        
        final_spikes1=transform.scale(initial_spikes,(524,10))
        final_spikes2=transform.scale(initial_spikes,(50,10))
        final_spikes3=transform.scale(initial_spikes,(100,10))
        final_spikes4=transform.scale(initial_spikes,(100,10))
        final_spikes4=transform.rotate(final_spikes4,(180))
        final_spikes5=transform.scale(initial_spikes,(70,10))
        final_spikes6=transform.scale(initial_spikes,(100,10))

        screen.blit(final_spikes1,(500,758))
        screen.blit(final_spikes2,(450,500))
        screen.blit(final_spikes3,(280,610))
        screen.blit(final_spikes4,(280,450))
        screen.blit(final_spikes5,(430,415))
        screen.blit(final_spikes6,(660,450))
        
        moveGuy(guy)
        checkCollision(guy,level_three_platforms,spikes)
        fireballs()
        lasers(768,player_locations)
        draw.line(screen,RED,(laser_x,laser_y),(x,768))
        screen.blit(pics[move][int(frame)],(guy[X],guy[Y]))

        for fireball in fireRects_lvl3:
            draw.rect(screen,(255,140,0),fireball)

        if rec.collidepoint(300,310-31):
            guy[X]=50
            guy[Y]=500
            starting_point=35
            ending_point=545
            return "level_four"

        
        myClock.tick(60)
        display.flip()
    return "menu"

                # [x, y, horizontal speed, vertical speed]
playerShuriken=[]
rapid=20
v=[2,0]

level_four_platforms=[Rect(150,758,1024-150,10),Rect(900,700,40,10),
                      Rect(970,620,40,10),Rect(900,540,40,10),
                      Rect(0,450,1024-150,10),Rect(0,380,30,10),
                      Rect(150,310,1024-50,10),Rect(982,240,60,10),
                      Rect(0,160,900,10)]

plat_1=[874,450]
plat_2=[150,310]
plat_3=[900,160]

##DEFINING ENEMIES ON A CERTAIN PLATFORM##
enemies_4_1=[Rect(400,450-31,18,31),Rect(600,450-31,18,31),Rect(700,450-31,18,31),Rect(300,450-31,18,31)]
enemies_4_2=[Rect(300,310-31,18,31),Rect(500,310-31,18,31),Rect(700,310-31,18,31),Rect(1000,310-31,18,31)]
enemies_4_3=[Rect(0,160-31,18,31),Rect(200,160-31,18,31),Rect(400,160-31,18,31),Rect(600,160-31,18,31),Rect(750,160-31,18,31)]

enemies_4_1_points=[[400,450-31],[600,450-31],[700,450-31],[300,450-31]]
enemies_4_2_points=[[300,310-31],[500,310-31],[700,310-31],[1000,310-31]]
enemies_4_3_points=[[0,160-31],[200,160-31],[400,160-31],[600,160-31],[750,160-31]]

def moveShuriken(player_weapon):
    
    rec=Rect(guy[X],guy[Y],18,31)
    mx,my=mouse.get_pos()
          
    for p in player_weapon:
        if p[4]==1:#checks to see of the mouse pointer position is greater the player position or not
            p[0]+=p[2]#moving the bullet depending on mouse and player position
            p[1]+=p[3]
            if p[0]>1024:
                player_weapon.remove(p) #removing the off-screen bullets
                    
        elif p[4]==-1:
            p[0]-=p[2]
            p[1]-=p[3]
            if p[0]<0:
                player_weapon.remove(p) #removing the off-screen bullets
    
def moveEnemy():

    global enemies_4_1,enemies_4_2,enemies_4_3,level_four_platforms,plat_1,plat_2,plat_3,enemies_4_1_points,enemies_4_2_points,enemies_4_3_points

    for enemy in enemies_4_1:#this is for the enemies on the certain platform 
        enemy.right+=3#moves the enemy to the right
        if enemy.right>plat_1[0]:#checks to see of the enemy reached the edge of the platform
            while enemy.left>0:
                enemy.left-=5#goes back to the beginning of the platform

    for enemy in enemies_4_2:
        enemy.right-=3
        if enemy.right<plat_2[0]:
            while enemy.right<1024:
                enemy.left+=5
                
    for enemy in enemies_4_3:
        enemy.right+=3
        if enemy.right>plat_3[0]:
            while enemy.left>0:
                enemy.left-=5

    for point in enemies_4_1_points:
        point[0]+=3
        if point[0]+18>plat_1[0]:
            while point[0]>0:
                point[0]-=5

    for point in enemies_4_2_points:
        point[0]+=3
        if point[0]+18>plat_1[0]:
            while point[0]>0:
                point[0]-=5

    for point in enemies_4_3_points:
        point[0]+=3
        if point[0]+18>plat_1[0]:
            while point[0]>0:
                point[0]-=5

collision=[]#list that checks how many times the player gets hit by enemy. If it reaches a certain #, then the player dies and starts over
count=20#the count variable delays elements appending to a list so that the player doesnt die quickly

def enemyCollision():#THIS FUNCTION WORKS ON THE ENMEMIES "KILLING" THE PLAYER

    global enemies_4_1,enemies_4_2,enemies_4_3,level_four_platforms,plat_1,plat_2,plat_3,collision,starting_point,count,ending_point
    rec=Rect(guy[X],guy[Y],18,31)

    for enemy in enemies_4_1:
        if rec.colliderect(enemy) and count==20:
            count=0#count will go to zero then will go to 20 to enable some delay
            collision.append("c")#adds a element to a list
            if len(collision)==10:#if you collide with the enemy 10 times even with delay thanks to count variable
                guy[X]=starting_point#you start the level again
                guy[Y]=ending_point+45
                del collision[:]#deletes all elements in list so it can count to 10 again
        if count<20:
            count+=1
    for enemy in enemies_4_2:
        if rec.colliderect(enemy) and count==20:
            count=0
            collision.append("c")
            if len(collision)==10:
                guy[X]=starting_point
                guy[Y]=ending_point+45
                del collision[:]
        if count<20:
            count+=1
    for enemy in enemies_4_3:
        if rec.colliderect(enemy) and count==20:
            count=0
            collision.append("c")
            if len(collision)==10:
                guy[X]=starting_point
                guy[Y]=ending_point+45
                del collision[:]
        if count<20:# if there is collision count goes back to zero so this brings it back to 20
            count+=1

##THESE LISTS COUNT HOW MANY TIMES THE ENEMY GETS IT. IF THE ENEMY GETS HIT A CERTAIN # OF TIMES, THE ENEMY DIES AND IS DELETED       
bulletCollision1=[]
bulletCollision2=[]
bulletCollision3=[]
bulletCollision4=[]
bulletCollision5=[]
bulletCollision6=[]
bulletCollision7=[]
bulletCollision8=[]
bulletCollision9=[]
bulletCollision10=[]
bulletCollision11=[]
bulletCollision12=[]
bulletCollision13=[]
element=0
checkingCompletion=[]#THIS LIST CHECKS IF YOU KILLED ALL THE ENEMIES. YOU NEED TO KILL THEM ALL TO ADVANCE TO NEXT LEVEL
def shurikenCollision():#FUNCTION WORKS ON PLAYER "KILLING" THE ENEMIES USING BULLETS
    global enemies_4_1,enemies_4_2,enemies_4_3,playerShuriken,bulletCollision1,bulletCollision2,bulletCollision3,bulletCollision4,bulletCollision5,element
    global bulletCollision1,bulletCollision1,bulletCollision1,bulletCollision1,bulletCollision1,bulletCollision1,bulletCollision1,bulletCollision1,count
    global checkingCompletion
    rec=Rect(guy[X],guy[Y],18,31)
    for p in playerShuriken:
        shuriken=Rect(int(p[0]),int(p[1]),8,8)
        if shuriken.colliderect(enemies_4_1[element]) and count==20:#checks if the bullet hits the enemy
            bulletCollision1.append("b")#this is the counter of how many times the enemy gets hit
            count=0
            playerShuriken.remove(p)#removes bullet so it doesnt go through the enemy
            if len(bulletCollision1)==5:#if the enemy gets hit 5 times
                enemies_4_1[0]=Rect(0,0,0,0)#enemy is deleted
                checkingCompletion.append("q")#one enemy dies, one element is added to this list to keep track of how many enemies has the player killed
        if shuriken.colliderect(enemies_4_1[element+1]) and count==20:
            bulletCollision2.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision2)==5:
                enemies_4_1[1]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_1[element+2]) and count==20:
            bulletCollision3.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision3)==5:
                enemies_4_1[2]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_1[element+3]) and count==20:
            bulletCollision4.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision4)==5:
                enemies_4_1[3]=Rect(0,0,0,0)
                checkingCompletion.append("q")

        if shuriken.colliderect(enemies_4_2[element]) and count==20:
            bulletCollision5.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision5)==5:
                enemies_4_2[0]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_2[element+1]) and count==20:
            bulletCollision6.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision6)==5:
                enemies_4_2[1]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_2[element+2]) and count==20:
            bulletCollision7.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision7)==5:
                enemies_4_2[2]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_2[element+3]) and count==20:
            bulletCollision8.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision8)==5:
                enemies_4_2[3]=Rect(0,0,0,0)
                checkingCompletion.append("q")

        if shuriken.colliderect(enemies_4_3[element]) and count==20:
            bulletCollision9.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision9)==5:
                enemies_4_3[0]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_3[element+1]) and count==20:
            bulletCollision10.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision10)==5:
                enemies_4_3[1]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_3[element+2]) and count==20:
            bulletCollision11.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision11)==5:
                enemies_4_3[2]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_3[element+3]) and count==20:
            bulletCollision12.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision12)==5:
                enemies_4_3[3]=Rect(0,0,0,0)
                checkingCompletion.append("q")
        if shuriken.colliderect(enemies_4_3[element+4]) and count==20:
            bulletCollision13.append("b")
            count=0
            playerShuriken.remove(p)
            if len(bulletCollision13)==5:
                enemies_4_3[4]=Rect(0,0,0,0)
                checkingCompletion.append("q")

        if count<20:#DELAY
            count+=2

def level_four():

    global playerShuriken,rapid,v,checkingCompletion
    running = True
    myClock = time.Clock()
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

        level_four_platforms=[Rect(150,758,1024-150,10),Rect(900,700,40,10),#platforms that are drawn in the level
                      Rect(970,620,40,10),Rect(900,540,40,10),
                      Rect(0,450,1024-150,10),Rect(0,380,30,10),
                      Rect(150,310,1024-50,10),Rect(982,240,60,10),
                      Rect(0,160,900,10)]

        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        screen.fill(BLACK)
        rec=Rect(guy[X],guy[Y],18,31)
        draw.rect(screen,BLACK,rec)

        for i in range(len(level_four_platforms)):
            draw.rect(screen,BLACK,level_four_platforms[i])

        finalPlatform1=transform.scale(initial_platforms,(1024-150,10))
        finalPlatform2=transform.scale(initial_platforms,(40,10))
        finalPlatform3=transform.scale(initial_platforms,(40,10))
        finalPlatform4=transform.scale(initial_platforms,(40,10))
        finalPlatform5=transform.scale(initial_platforms,(1024-150,10))
        finalPlatform6=transform.scale(initial_platforms,(30,10))
        finalPlatform7=transform.scale(initial_platforms,(1024-50,10))
        finalPlatform8=transform.scale(initial_platforms,(60,10))
        finalPlatform9=transform.scale(initial_platforms,(900,10))

        screen.blit(finalPlatform1,(150,758))
        screen.blit(finalPlatform2,(900,700))
        screen.blit(finalPlatform3,(970,620))
        screen.blit(finalPlatform4,(900,540))
        screen.blit(finalPlatform5,(0,450))
        screen.blit(finalPlatform6,(0,380))
        screen.blit(finalPlatform7,(150,310))
        screen.blit(finalPlatform8,(982,240))
        screen.blit(finalPlatform9,(0,160))

        if mb[0]==1 and rapid==20:
            rapid=0
            v[0]=5
            v[1]=0
            if mx>guy[X]:#you need to use pointer to change direction of where the player shoots
                playerShuriken.append([guy[X]+20,guy[Y]+16,v[0],v[1],1])#last element is used to check mouse pos
            else:
                playerShuriken.append([guy[X]+20,guy[Y]+16,v[0],v[1],-1])

        if rapid<20:
            rapid+=1
            
        spikes=[Rect(0,0,0,0)]

        screen.blit(pics[move][int(frame)],(guy[X],guy[Y]))
        moveGuy(guy)
        checkCollision(guy,level_four_platforms,spikes)
        moveShuriken(playerShuriken)
        moveEnemy()
        enemyCollision()
        shurikenCollision()

        for i in range(len(enemies_4_1)):
            draw.rect(screen,WHITE,enemies_4_1[i])

        for i in range(len(enemies_4_2)):
            draw.rect(screen,WHITE,enemies_4_2[i])

        for i in range(len(enemies_4_3)):
            draw.rect(screen,WHITE,enemies_4_3[i])

        for p in playerShuriken:
            shuriken=Rect(int(p[0]),int(p[1]),8,8)
            draw.rect(screen,GREEN,shuriken)

        for i in range(len(spikes)):
            draw.rect(screen,BLUE,spikes[i])
            
        if rec.collidepoint(10,160-31) and len(checkingCompletion)==13:#there are 13 enemies in level 4. To complete this level, you need to kill all 13
            return "level_five"

        myClock.tick(60)
        display.flip()
    return "menu"

bossPointx,bossPointy=500,300#final boss initial points
timer=0#counts the number of seconds

##KEEPS TRACK OF # OF TIMES YOU OR ENEMY IS HIT##
fireballCollision=[]
playerBulletCollision=[]

def level_five():

    global playerShuriken,v,finalboss,bossPointx,bossPointy,timer,fireballCollision

    rapid = 0# this variable like count is the "delay" of the bullets
    rapidBoss = 0# this variable like count is the "delay" of the bullets
    bullets = []
    bossFireball=[]

    running = True
    myClock = time.Clock()
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()

        screen.fill(BLACK)
        rec=Rect(guy[X],guy[Y],18,31)
        draw.rect(screen,BLACK,rec)
        screen.blit(pics[move][int(frame)],(guy[X],guy[Y]))

        keys = key.get_pressed()
        
        if rapid>0:#DELAY
            rapid-=1
            
        if mb[0]==1 and rapid==0:
            rapid = 50
            ang = atan2(my-guy[Y],mx-guy[X])#finds angle
            vx = cos(ang)*2#HORIZONTAL COMPONENT
            vy = sin(ang)*2#VERTICAL COMPONENT
            bullets.append([guy[X],guy[Y],vx,vy])#adds the "path" of the bullets using starting point and ending point

        for b in bullets:
            b[2]*=1.01#speeds up the bullets
            b[3]*=1.01
            b[0]+=b[2]#the bullets follow the "path"
            b[1]+=b[3]
            if b[0]>1024 or b[0]<0 or b[1]>768 or b[1]<0:
                bullets.remove(b)#bullets are removed if they leave the screen

        for b in bullets:
            playerBullet=Rect(int(b[0]),int(b[1]),4,4)
            draw.rect(screen,GREEN,playerBullet)
            if playerBullet.colliderect(finalboss):
                playerBulletCollision.append("p")#just like with enemies in lvl 4, this checks the amount of times you hit the final boss
                if len(playerBulletCollision)==25:#reaching this number of collisions will kill the final boss
                    return "you_win"
           
        timer+=1
        if timer%120==0:#after every 2 seconds...
            #THE FINAL BOSS OF THIS GAME WILL MOVE TO RANDOM POSITIONS ON THE SCREEN
            bossPointx=randint(-5,1030)
            bossPointy=randint(-5,773)

        if rapidBoss>0:#DELAY
            rapidBoss-=1

        if rapidBoss==0:
            rapidBoss = 50
            if guy[X]>bossPointx:
                angBoss = atan2(guy[Y]-bossPointy,guy[X]-bossPointx)
                bx = cos(angBoss)*2#HORIZONTAL COMPONENT
                by = sin(angBoss)*2#VERTICAL COMPONENT
                bossFireball.append([bossPointx,bossPointy,bx,by])
            else:
                angBoss = atan2(guy[Y]-bossPointy,guy[X]-bossPointx)
                bx = cos(angBoss)*2#HORIZONTAL COMPONENT
                by = sin(angBoss)*2#VERTICAL COMPONENT
                bossFireball.append([bossPointx,bossPointy,bx,by])
                
        for ball in bossFireball:
            ball[2]*=1.01
            ball[3]*=1.01
            ball[0]+=ball[2]
            ball[1]+=ball[3]
            if ball[0]>1024 or ball[0]<0 or ball[1]>768 or ball[1]<0:
                bossFireball.remove(ball)#removes fireballs that are not on the screen
                
        for ball in bossFireball:
            fireball=Rect(int(ball[0]),int(ball[1]),20,20)
            draw.rect(screen,(255,140,0),fireball)#draws the shooting fireballs

            if rec.colliderect(fireball):#if the player hits the fireballs
                fireballCollision.append("f")#just like with enemies in lvl 4, this counts the amount of times you are hit

                if len(fireballCollision)==50:#after this many collisions, you die and go back to lvl 1
                    fireballCollision=[]
                    return "level_one"

        finalboss=Rect(bossPointx,bossPointy,50,100)
        draw.rect(screen,BLACK,finalboss)
        final_bossPic=transform.scale(initial_boss,(50,100))
        screen.blit(final_bossPic,(bossPointx,bossPointy))
        moveGuy(guy)
            
        myClock.tick(60)
        display.flip()
    return "menu"

def menu():

    running = True
    myClock = time.Clock()

    title=image.load("the_great_escape.png")
    bg=image.load("menu_bg.png")
    bg=transform.scale(bg,(1024,768))
    play=image.load("PLAY.png")
    play=transform.scale(play,(200,80))
    instructions=image.load("how_to_play.png")
    instructions=transform.scale(instructions,(200,80))
    creds=image.load("credits_image.png")
    creds=transform.scale(creds,(200,80))
    obj=image.load("OBJECTIVE.png")
    obj=transform.scale(obj,(200,80))

    buttons=[Rect(250,195,200,80),Rect(250,355,200,80),Rect(550,195,200,80),Rect(550,355,200,80)]#the buttons you can click on menu
    vals = ["level_one","credits","instructions","story"]#what each click of a button can lead to
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(bg,(0,0))
        screen.blit(title,(70,60))
        for i in range(len(buttons)):
            draw.rect(screen,BLACK,buttons[i])
            if buttons[i].collidepoint(mpos):#buttons are highlighted when hovered over
                draw.rect(screen,RED,buttons[i],3)
                if mb[0]==1:
                    return vals[i]#goes to that page when you click a button
            else:
                draw.rect(screen,BLACK,buttons[i],2)

        screen.blit(play,(250,200))
        screen.blit(instructions,(550,200))
        screen.blit(creds,(250,360))
        screen.blit(obj,(550,360))
            
        display.flip()

def credit():
    running = True
    cred = image.load("credits.png")
    cred = transform.scale(cred,(1024,768))
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"

def instructions():
    running = True
    inst = image.load("instructions.png")
    inst = transform.scale(inst,(1024,768))
    screen.blit(inst,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"

def story():
    running = True
    story = image.load("story.png")
    story = transform.scale(story,(1024,768))
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
    return "menu"

def you_win():
    running = True
    winner = image.load("you_win.png")
    winner = transform.scale(winner,(1024,768))
    screen.blit(winner,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
    return "menu"


def checkCollision(guy,plats,sharp_object):

    global fireRects
    global page

    rec=Rect(guy[X],guy[Y],18,31)

    for p in plats:
        if rec.colliderect(p):
            if guy[VY]>=0 and rec.move(0,-guy[VY]).colliderect(p)==False:
                guy[ONGROUND]=True
                guy[VY]=0
                guy[Y]=p.y-31
    
    if guy[X]<0 and guy[X]>1024:
        guy[X]-=0#this prevents the player from leaving the screen

    for s in sharp_object:
        if rec.colliderect(s):#if the player collides with the spikes, you start the level again
            guy[X]=starting_point
            guy[Y]=ending_point

    for fireball in fireRects:
        if rec.colliderect(fireball) and page=="level_two":#if you hit the fireballs in lvl 2, you die
            guy[X]=starting_point
            guy[Y]=ending_point
        if (rec.colliderect(fireRects_lvl3[0]) or rec.colliderect(fireRects_lvl3[1])) and page=="level_three":
            guy[X]=starting_point
            guy[Y]=ending_point
    
screen = display.set_mode((1024, 768))
running = True
x,y = 0,0
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "level_one":
        page = level_one()
    if page == "level_two":
        page = level_two()
    if page == "level_three":
        page = level_three()
    if page == "level_four":
        page = level_four()
    if page == "level_five":
        page = level_five()
    if page == "credits":
        page = credit()
    if page == "instructions":
        page = instructions()
    if page == "story":
        page == story()
    if page == "you_win":
        page = you_win()

quit()