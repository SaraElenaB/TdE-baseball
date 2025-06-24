from database.DB_connect import DBConnect
from model.teams import Teams


class DAO():

    @staticmethod
    def getAllAnni():
        conn = DBConnect.get_connection()
        ris=[]
        cursor = conn.cursor(dictionary=True)

        query=""" select distinct t.`year`
                  from teams t 
                  where t.`year`>=1980
                  order by  t.`year`DESC"""
        cursor.execute(query)

        for row in cursor:
            ris.append( row["year"])

        cursor.close()
        conn.close()
        return ris

    # ---------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getSquadreAnno(anno):
        conn = DBConnect.get_connection()
        ris = []
        cursor = conn.cursor(dictionary=True)

        query = """ select *
                    from teams t
                    where t.`year` = %s"""
        cursor.execute(query, (anno,))

        for row in cursor:
            ris.append( Teams(**row))

        cursor.close()
        conn.close()
        return ris

    # ---------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getSalarioGiocatoriSquadra(anno, idMapSalari):
        conn = DBConnect.get_connection()
        ris = {}
        cursor = conn.cursor(dictionary=True)

        query = """ select t.teamCode, t.ID sum(s.salary) as salarioTotSquadra
                    from salaries s , appearances a , teams t 
                    where s.`year` = 2015
                    and s.`year` = a.`year`
                    and s.`year` = t.`year`
                    and a.teamID = t.ID
                    and a.playerID = s.playerID
                    group by t.teamCode, t.name"""
        cursor.execute(query, (anno,))
        # essenzialmente devo collegare Salary e Teams e lo faccio tramite Appearances -->
        # prendi i dati dalle tabelle che hanno sicuramente tutti i valori!!!

        for row in cursor:
            ris[idMapSalari[row["ID"]]] = row["salarioTotSquadra"]

        cursor.close()
        conn.close()
        return ris
    # ---------------------------------------------------------------------------------------------------------------------------
