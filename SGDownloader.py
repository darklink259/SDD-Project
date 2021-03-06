import pygame
from gbxml import list_remote_xml_files
from gbxml import download
from gbxml import upload

class LineItem(object):
    
    
    def __init__(self, pos, text, res, id):
        """One study guide line item"""
        self.rect = pygame.Rect(pos, res)
        self.font = pygame.font.SysFont("Courier", 20)
        temp = text.replace("xml/", "")
        self.fontSurf = self.font.render(temp, False, (0,0,0))
        self.sprite = pygame.image.load("gfx/lineItem.png").convert_alpha()
        self.id = id
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left, self.rect.top), self.fontSurf.get_rect())
        
    def click_check(self, pos):
        return self.rect.collidepoint(pos)
        
    def getID(self):
        return self.id
     
     
class LoaderPopup(object):
    
    def __init__(self, pos, res, loaded):
        """Defines the success/fail of the operation"""
        self.rect = pygame.Rect(pos, res)
        self.font = pygame.font.SysFont("Courier", 16)
        if loaded == -1:
            self.fontSurf = self.font.render("Could not get server files", False, (0,0,0))
        elif loaded:
            self.fontSurf = self.font.render("Guide downloaded successfully.", False, (0,0,0))
        else:
            self.fontSurf = self.font.render("Failed download of selected file.", False, (0,0,0))
        self.sprite = pygame.image.load("gfx/loaderPopup.png").convert_alpha()
        
    def draw(self,screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left + self.rect.width/2.0 - self.fontSurf.get_rect().width/2.0, self.rect.top + self.rect.height/2.0 - self.fontSurf.get_rect().height/2.0),
        self.fontSurf.get_rect())
        
    def click_check(self, pos):
        return self.rect.collidepoint(pos)


        
class SGDownloader(object):
    
    __res = (600, 400)
    __lineItemOffset = 20
    __separationLine = 5
    __popup_res = (300, 200)
    
    def __init__(self, screenSize):
        """Downloads guides from the server to the local client"""
        self.rect = pygame.Rect(((screenSize[0] - self.__res[0]) / 2, (screenSize[1] - self.__res[1]) / 2), self.__res)
        self.sprite = pygame.image.load("gfx/guideLoader.png").convert_alpha()
        self.screenSize = screenSize
        self.files = list_remote_xml_files()
        self.selectionIndex = -1
        self.loadSuccess = False
        self.loadPopup = False
        
        self.lineItems = []
        for i in range(0, len(self.files)):
            if i == 0:
                 self.lineItems.append(LineItem((self.rect.topleft[0], self.rect.topleft[1]), self.files[i], (self.__res[0], self.__lineItemOffset), i))
            else:
                self.lineItems.append(LineItem((self.rect.topleft[0], self.rect.topleft[1] +  self.__lineItemOffset * i + self.__separationLine * i),
                self.files[i], (self.__res[0], self.__lineItemOffset), i))
                
    def update(self):
        if not self.files:
            self.loadPopup = LoaderPopup((self.screenSize[0]/2 - self.__popup_res[0]/2, self.screenSize[1]/2 - self.__popup_res[1]/2), self.__popup_res, -1)
        elif self.selectionIndex > -1:
            self.loadSuccess = download(self.files[self.selectionIndex])    
            self.selectionIndex = -1
            self.loadPopup = LoaderPopup((self.screenSize[0]/2 - self.__popup_res[0]/2, self.screenSize[1]/2 - self.__popup_res[1]/2), self.__popup_res, self.loadSuccess)
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        for l in self.lineItems:
            l.draw(screen)
        if self.loadPopup:
            self.loadPopup.draw(screen)
        
    def process_events(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if not self.loadPopup:
                    for l in self.lineItems:
                        if(l.click_check(event.pos)):
                            self.selectionIndex = l.getID()
                else:
                    if(self.loadPopup.click_check(event.pos)):
                        run = False
                        
        return run                