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

    @staticmethod
    def getSalarioGiocatoriSquadra(anno, idMapSalari):
        conn = DBConnect.get_connection()
        ris = {}
        cursor = conn.cursor(dictionary=True)

        query = """ select t.teamCode, t.ID, sum(s.salary) as sumGiocatoriSquadra
                    from salaries s , teams t, appearances a 
                    where a.`year` = t.`year`and t.`year` = s.`year`
                    and a.`year` = %s
                    and t.ID = a.teamID
                    and a.playerID = s.playerID
                    group by t.teamCode"""
        cursor.execute(query, (anno,))

        for row in cursor:
            ris[idMapSalari[row["ID"]]] = row["sumGiocatoriSquadra"]

        cursor.close()
        conn.close()
        return ris
