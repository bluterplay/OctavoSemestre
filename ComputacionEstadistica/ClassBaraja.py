import numpy as np

class ManoPoker:

    def __init__(self):
        self.mano=[]
        self.deck = []
        self.valores={}
        self.palos={}
        
    def set_deck(self):
        ls_palos= ["Trebol", "Espada", "Corazón", "Diamante"]
        ls_numeros=  ["AS"]+ [str(x) for x in range(2,11)] +[ "J","Q", "K"]
        ls_deck=[x+' '+ y for x in ls_numeros for y in ls_palos]
        deck = list(np.random.choice(ls_deck,size=52,replace= False))
        self.deck= deck
        
    def update_deck(self,mano):
        for carta in mano:
            self.deck.remove(carta)
    
    def get_deck(self):
        return self.deck
    
    def get_cards(self,n):
        if(len(self.deck)<n):
            return False
        else:
            ls_manos= []
            ls_deck = self.deck
            mano=ls_deck[0:5]
            self.mano= mano
            self.update_deck(mano)
            return mano
    
    def get_mapeo(self):
        ls_palos= ["Trebol", "Espada", "Corazón", "Diamante"]
        ls_numeros=  ["AS"]+ [str(x) for x in range(2,11)] +[ "J","Q", "K"]
        dc_valores= {card: valor for (card,valor) in list(zip(ls_numeros,range(0,13)))}
        dc_palos = {palo: valor for (palo,valor) in list(zip(ls_palos, range(0,4)))}
        self.valores= dc_valores
        self.palos= dc_palos
        ls_valor=[0 for x in range(13)]
        ls_palo=[0 for x in range(4)]
        for card in self.mano:
            card= card.split(" ")
            valor= card[0]
            palo= card[1]
            ls_valor[dc_valores[valor]]+= 1
            ls_palo[dc_palos[palo]]+=1
        return np.array(ls_valor), np.array(ls_palo)
    
    def get_key(self,val):
        for key, value in self.valores.items():
            if val == value:
                return key
        return "key doesn't exist"

    def alta(self,ls_valor):
        if(ls_valor[0]==1):
             return'AS'
        else:
            for i in range(12,0,-1):
                if (ls_valor[i]!=0):
                    return self.get_key(i)
                
    def escalera(self,ls_valor):
        if(ls_valor[0]==1 and (ls_valor[9:13].min() >0)):
            return True
        else:
            for i in range(8):
                aux= ls_valor[i:(i+5)]
                if(aux.min()>0):
                    return True
            return False
    
    def color(self,ls_palo):
        if(ls_palo.max()<5):
            return False
        else: 
            return True
    
    def poker(self,ls_valor):
        if(ls_valor.max()<4):
            return False
        else:
            return True
    
    def par(self,ls_valor):
        par= 0
        total=0
        for valor in ls_valor:
            total+=valor
            if(valor==2):
                par+=1
            if(total==5):
                break
        if(par==1):
            return True
        elif(par==2):
            return "Doble"
        else:
            return False
    
    def tercia(self,ls_valor):
        if(ls_valor.max()<3):
            return False
        else:
            return True

    def full(self,ls_valor):
        if(self.par(ls_valor) and self.tercia(ls_valor)):
            return True
        else:
            return False
     
    def get_type_hand(self, ls_valor,ls_palo):
        if(self.color(ls_palo)):
            if(self.escalera(ls_valor)):
                if(ls_valor[0]==1and ls_valor[12]==1):
                    return("Escalera Real")
                else:
                    return("Escalera de color")
            else:
                return("Color")
        else:
            if(self.poker(ls_valor)):
                return("Pokar")
            else:
                if(self.full(ls_valor)):
                    return("Full")
                else:
                    if(self.escalera(ls_valor)):
                        return("Escalera")
                    else:
                        if(self.tercia(ls_valor)):
                            return("Tercia")
                        else:
                            if(self.par(ls_valor) =='Doble'):
                                return("Doble")
                            elif(self.par(ls_valor)):
                                return("Par")
                            else:
                                return("Alta")

mano=ManoPoker()
mano.set_deck()

dc={"Escalera Real":0, "Escalera de color":0, "Pokar":0,"Full":0,
    "Color":0,"Escalera":0, "Tercia":0, "Doble":0,"Par":0,"Alta":0 }

n= 1000000
for i in range(n):
    if( mano.get_cards(5)==False):
        mano=ManoPoker()
        mano.set_deck()
        mano.get_cards(5)

    ls_valor,ls_palo=mano.get_mapeo()
    dc[mano.get_type_hand(ls_valor,ls_palo)]+=1
probabilidad = {k: v/1000000 for k, v in dc.items()}

print("Despues de 100000 simulaciones tenemos que: ")
for key in probabilidad.keys():
    print(f'{key}: {dc[key]} veces, {probabilidad[key]*100} %')
