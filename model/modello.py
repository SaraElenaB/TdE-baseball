import copy
import itertools
import random
import warnings

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.Graph()
        nodes=[]
        self._idMapSquadreEffettive={}

        self._bestPath=[]
        self._bestScore=0 #peso massimo

    # ---------------------------------------------------------------------------------------------------------------------------
    def getAnni(self):
        return DAO.getAllAnni()

    def getSquadreAnno(self, anno):
        return DAO.getSquadreAnno(anno)

    # ---------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, anno):
        self._grafo.clear()
        nodes = DAO.getSquadreAnno(anno)
        #modo1
        # self._grafo.add_nodes_from(nodes)
        # for n1 in self._grafo.nodes:
        #     for n2 in self._grafo.nodes:
        #         if n1 != n2 and not self._grafo.has_edge(n1, n2):
        #             self._grafo.add_edge(n1, n2)

        #modo2
        for n1, n2 in itertools.combinations(nodes, 2):
            self._grafo.add_edge(n1, n2)

        for n in nodes:
            self._idMapSquadreEffettive[n.ID] = n

        print( f"Num nodi {len(self._grafo.nodes)} /nNum archi: {len(self._grafo.edges)}" )

        salarioDelleSquadre = DAO.getSalarioGiocatoriSquadra(anno, self._idMapSquadreEffettive)
        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salarioDelleSquadre[e[0]] + salarioDelleSquadre[e[1]]

        return self._grafo

    # ---------------------------------------------------------------------------------------------------------------------------
    def getGrafoDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    #---------------------------------------------------------------------------------------------------------------------------
    def getViciniOrdinati(self, source):
        #vicini = self._grafo.neighbors(source)
        vicini = nx.neighbors(self._grafo, source) # [ v0, v1, v2 ...]
        viciniTuple=[]

        for v in vicini:
            viciniTuple.append( (v, self._grafo[source][v]["weight"] ) )  #[ (v0,p0) , (v1,p1) , ....]

        viciniTuple = sorted( viciniTuple, key=lambda x: x[1], reverse=True)
        return viciniTuple

    # ---------------------------------------------------------------------------------------------------------------------------
    def getCamminoOttimoV1(self, source):

        self._bestPath=[]
        self._bestScore=0
        parziale= [source]

        vicini = nx.neighbors(self._grafo, source)
        for v in vicini:
            parziale.append(v)    #cosi lunghezza=2 [source, v]
            self._ricorsioneV1(parziale)
            parziale.pop()

        return self._bestPath , self._bestScore

    # ---------------------------------------------------------------------------------------------------------------------------
    def _ricorsioneV1(self, parziale):
        print(len(parziale))
        #1. terminale
            #parziale è una soluzione?
            #parziale è meglio della best
        if self.score(parziale) > self._bestScore:  #non ho vincoli sulla lunghezza, ma sul peso
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.score(parziale)

        #2. #ricorsione
            #posso aggiungere un nuovo nodo?
            #aggiungo nodo e faccio la ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            if (v not in parziale) and (self._grafo[parziale[-2]][parziale[-1]]["weight"] > self._grafo[parziale[-1]][v]["weight"]):  #già aggiunto > di quello che aggiiungo
                parziale.append(v)
                self._ricorsioneV1(parziale)
                parziale.pop()

    # ---------------------------------------------------------------------------------------------------------------------------
    def getCamminoOttimoV2(self, source):

        self._bestPath = []
        self._bestScore = 0
        parziale = [source]

        vicini = nx.neighbors(self._grafo, source)
        viciniTuple=[]
        for v in vicini:
            peso=self._grafo[source][v]["weight"]
            viciniTuple.append( (v,peso))

        viciniTuple.sort( key=lambda x: x[1], reverse=True)
        #non avendo altri archi --> non devo controlalre che il peso sia minore/maggiore
        #for v in vicini:
        parziale.append(viciniTuple[0][0]) #prendo il primo nodo
        self._ricorsioneV2(parziale)
        parziale.pop()
        return self.getPesiOfPath(self._bestPath) , self._bestScore

    # ---------------------------------------------------------------------------------------------------------------------------
    def _ricorsioneV2(self, parziale):
        print(len(parziale))
        # 1. terminale
            # parziale è una soluzione?
            # parziale è meglio della best
        if self.score(parziale) > self._bestScore:  # non ho vincoli sulla lunghezza, ma sul peso
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.score(parziale)

        # 2. #ricorsione
            # posso aggiungere un nuovo nodo?
            # aggiungo nodo e faccio la ricorsione
        vicini = nx.neighbors(self._grafo, parziale[-1])
        viciniTuple = []
        for v in vicini:
            peso = self._grafo[parziale[-1]][v]["weight"]
            viciniTuple.append( (v, peso) )
        viciniTuple.sort(key=lambda x: x[1], reverse=True)

        for t in viciniTuple:
            if ((t[0] not in parziale) and
                    (self._grafo[parziale[-2]][parziale[-1]]["weight"] > t[1])):  # già aggiunto > di quello che aggiiungo
                parziale.append(t[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return

    # ---------------------------------------------------------------------------------------------------------------------------
    def score(self, listaDiNodi):

        if len(listaDiNodi) < 2:
            warnings.warn("Errore in score, attesa lista più lunga")

        totPeso=0
        for i in range(len(listaDiNodi)-1):
            totPeso += self._grafo[listaDiNodi[i]][listaDiNodi[i+1]]["weight"]
        return totPeso

    # ---------------------------------------------------------------------------------------------------------------------------
    def getPesiOfPath(self, listaDiNodi):

        tuplePesi= [ (listaDiNodi[0], 0)]
        for i in range(1, len(listaDiNodi)):
            tuplePesi.append( (listaDiNodi[i], self._grafo[listaDiNodi[i-1]][listaDiNodi[i]]["weight"]) )
        return tuplePesi

    # ---------------------------------------------------------------------------------------------------------------------------
    def getRandomNode(self):
        index = random.randint(0,len(self._grafo.nodes)-1)
        return list(self._grafo.nodes)[index]

    # ---------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    m = Model()
    grafo = m.buildGraph(2015)
    print(f"Grafo {grafo}")

    source= m.getRandomNode()
    path, score = m.getCamminoOttimoV2(source)
    print(f"Lunghezza cammino: {len(path)} \nCostoOttmo: {score}")



