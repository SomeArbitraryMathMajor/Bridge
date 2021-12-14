##
##=======================================================
## Bryan Zang (20897536)
## CS 116 Spring 2021
## Final Project - Bridge Scoring
##=======================================================
##

from final_project3 import *
import check


def score(bridge_game):
  '''
  Returns the score of a bridge game.
  
  score: Game -> Int
  
  Examples:
     P = [Player("North", []), Player("East", []),  
          Player("South", []), Player("West", [])]  
     G = Game([Bid("3", "NT"), None], "South", 
         "North", 9, P, False, False)
     score(G) => 400
     
     G = Game([Bid("4", "S"), None], "South", 
         "North", 11, P, False, True)
     score(G) => 450
  
     G = Game([Bid("4", "S"), Bid("double", None)], 
              "South", "North", 9, P, True, False)
     score(G) => -200 
  '''
  contract_point = 0
  penalty_point = 0
  makes = bridge_game.declarer_tricks >= int(bridge_game.contract[0].value)
  if bridge_game.declarer in "NorthSouth":
    dec_vul = bridge_game.ns_vulnerable
  else:
    dec_vul = bridge_game.ew_vulnerable
  
  if makes: # makes or exceeeds contract
    overtrick = bridge_game.declarer_tricks > int(bridge_game.contract[0].value)
    doubled = bridge_game.contract[1].value == 'double' or\
      bridge_game.contract[1].value == 'redouble'
    
    if bridge_game.contract[0].suit in 'SH': # major suit
      contract_point = int(bridge_game.contract[0].value) * 30
    elif bridge_game.contract[0].suit in 'CD': # minor suit
      contract_point = int(bridge_game.contract[0].value) * 20
    else: # no trump
      contract_point = 40 + (int(bridge_game.contract[0].value)-1) * 30
    
    # double/redouble
    if doubled:
      # double
      if bridge_game.contract[1].value == 'double':
        contract_point *= 2
        doubled = True
      # redouble
      elif bridge_game.contract[1].value == 'redouble':
        contract_point *= 4
        doubled = True
    # None has no effect
      
    # game bonus
    if contract_point < 100:
      contract_point += 50
    else:
      contract_point += 300   
    
    # overtrick
    if overtrick: # tricks > contract
      if doubled: # doubled or redoubled
        if bridge_game.contract[1].value == 'double':
          if dec_vul: # vulnerable double
            contract_point += 200
          else: # not vulnerable double
            contract_point += 100
          # bonus point for double
          contract_point += 50
        else: # redouble
          if dec_vul: # vulnerable redouble
            contract_point += 400
          else: # not vulnerable redouble
            contract_point += 200
          # bonus point for redouble
          contract_point += 100
      
      else: # no double or redouble
        if bridge_game.contract[0].suit in 'SHNT':
          contract_point += bridge_game.declarer_tricks -\
                             (int(bridge_game.contract[0].value) * 30)
        else:
          contract_point += bridge_game.declarer_tricks -\
                             (int(bridge_game.contract[0].value) * 20)     
      
    # slam bonus
    if bridge_game.contract[0].value == '6': # small slam
      if dec_vul:
        contract_point += 750
      else:
        contract_point += 500
    elif bridge_game.contract[0].value == '7': # grand slam
      if dec_vul:
        contract_point += 1500
      else:
        contract_point += 1000
      
      return contract_point
  else: # does not make contract
    undertrick = int(bridge_game.contract[0].value)-bridge_game.declarer_tricks
    if dec_vul: # declaring team vulnerable
      if bridge_game.contract[1].value == 'double': # double
        if undertrick == 1: # 1 undertrick
          penalty_point += 200
        else: # 2 or more
          penalty_point += 300
      elif bridge_game.contract[1].value == 'redouble': # redouble
        if undertrick == 1: # 1 undertrick
          penalty_point += 400
        else: # 2 or more
          penalty_point += 600
      else: # none
        penalty_point += 100
    
    else: # declaring team not vulnerable
      if bridge_game.contract[1].value == 'double': # double
        if undertrick == 1: # 1 undertrick
          penalty_point += 100
        elif undertrick < 4: # 2 to 3
          penalty_point += 200
        else: # 4 or more
          penalty_point += 300
      elif bridge_game.contract[1].value == 'redouble': # redouble
        if undertrick == 1: # 1 undertrick
          penalty_point += 200
        elif undertrick < 4: # 2 to 3
          penalty_point += 400
        else: # 4 or more
          penalty_point += 600
      else: # none
        penalty_point += 50
    
    return penalty_point * -1


##Examples for score
P = [Player("North", []), Player("East", []),  Player("South", []),
     Player("West", [])]  
G = Game([Bid("3", "NT"), None], "South", 
    "North", 9, P, False, False)
check.expect("Example 1", score(G), 400)

G = Game([Bid("4", "S"), None], "South", 
    "North", 11, P, False, True)
check.expect("Example 2", score(G), 450)

G = Game([Bid("4", "S"), Bid("double", None)], "South", 
    "North", 9, P, True, False)
check.expect("Example 3", score(G), -200)


##To see the whole game in action, uncomment this to play!
print(score(play_game_bootstrap()))