import itertools
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.Graph()
        nodes=[]
        self._idMapSquadreEffettive={}

    def getAnni(self):
        return DAO.getAllAnni()

    def getSquadreAnno(self, anno):
        return DAO.getSquadreAnno(anno)

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

    # ---------------------------------------------------------------------------------------------------------------------------
    def getGrafoDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
    #---------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    m = Model()
    grafo = m.buildGraph(2015)
    print(grafo)



