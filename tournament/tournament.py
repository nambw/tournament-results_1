#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# Template provided by Udacity
# Modified to define required DB API
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        DB = psycopg2.connect("dbname=tournament")
        c = DB.cursor()
        return DB, c 
    except:
        print "Error connecting to the database."      
        raise 

def deleteMatches():
    """Remove all the match records from the database."""
    DB, c  =  connect()
    try:
	query = " DELETE FROM Match;"
    	c.execute(query)
	DB.commit()
    except:
        print "Error deleting table Match from database."	
    finally:
        c.close()
        DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB, c  =  connect()
    try:
       query = " DELETE FROM Players;"
       c.execute(query)
       DB.commit()
    except:
        print "Error deleting Players."	
    finally:
        c.close()
        DB.close()

def countPlayers():
   """Returns the number of players currently registered."""
   DB, c  =  connect()
   query = "Select * FROM Players;"
   c.execute(query)
   result = c.fetchall();
   count = c.rowcount
   print "There are" + str(count) + "registered players"
   DB.close()
   return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    sql = "INSERT INTO players (playerName) values (%s)"
    c.execute(sql, (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect();
    query = "SELECT * FROM p_standing;"
    c.execute(query)
    result = c.fetchall()
    DB.close()
    return result

def playerStandingsOld():
    """Returns a list of the players and their win records, sorted by wins.
    Unused function as the functionality is defined better using views in above function
    """
    DB, c = connect();
    query = "SELECT p.playerId, p.playerName, u.wins, u.wins + u.loss \
            FROM Players AS p JOIN (SELECT a.id as id , a.loss as loss , b.wins as wins \
                          FROM (SELECT Players.playerId AS id, COUNT(m.matchid) AS loss \
                                FROM Players LEFT JOIN Match as m ON (Players.playerId = m.loserid) GROUP BY id \
                               ) AS a \
                          JOIN (SELECT Players.playerId AS id, COUNT(m.matchid) AS wins \
                                FROM Players LEFT JOIN Match as m ON (Players.playerId = m.winnerid) GROUP BY id \
                               ) AS b \
                          ON (a.id = b.id)) AS u \
                     ON (p.playerId = u.id)\
                     ORDER BY u.wins  DESC; "

    c.execute(query)
    result = c.fetchall()
    DB.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB,c = connect();
    sql = "INSERT INTO Match (WinnerId, LoserId) values (%s, %s)"
    c.execute(sql, (winner,loser,))
    DB.commit()
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    if len(standings) < 2:
        print("Not enough Players.")
        return None
    pair = []
    for i in range(0, len(standings), 2):
        pair.append ((standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]))
    return pair

