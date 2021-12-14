##
##=======================================================
## Bryan Zang (20897536)
## CS 116 Spring 2021
## Final Project - Bridge Bidding
##=======================================================
##

from final_project import*
import check

class Bid:
  '''
  Fields:
     value (Str)
     suit (anyof Str None)
  Requires:
     value is one of "1", "2", "3", "4", "5", "6", "7", 
         "pass", "double", "redouble"
     suit is one of "C", "D", "H", "S", "NT" or None
     If value is non-numeric, then suit must be None
  '''
  
  def __init__(self, bid_value, bid_suit):
    '''
    Initialized a valid Bridge bid.
   
    Effects: Mutates self
  
    __init__: Bid Str (anyof Str None) -> None
    Requires: Conditions from Fields above are met.
    '''
    self.value = bid_value
    self.suit = bid_suit

  def __repr__(self):
    '''
    Returns a representation of a Card object
  
    __repr__: Card -> Str
    '''
    if self.suit == None:
      return "{0.value}".format(self)
    return "{0.value}{0.suit}".format(self)
    
  def __eq__(self, other):
    '''
    Returns True if self and other have equal values and suits 
    and False otherwise
  
    __eq__: Bid Any -> Bool
    '''
    return isinstance(other, Bid) and\
           self.value == other.value and\
           self.suit == other.suit
  
  def __lt__(self, other):
    '''
    Returns True if both self and other are numeric bids and
    self is a bid that comes before other. False otherwise
  
    __lt__: Bid Any -> Bool
    '''
    if not self.value.isdigit() or not other.value.isdigit():
      return False
    else:
      if self.value > other.value:
        return True
      elif self.value == other.value:
        if self.suit == 'NT':
          return False
        elif other.suit == 'NT':
          return True
        else:
          return self.suit < other.suit
      else:
        return False
      
  
def valid_bid(bids, new_bid):
  '''
  Returns True if new_bid is allowed in a Bridge
  game given the previous bids in bids. False otherwise
  
  valid_bid: (listof Bid) Bid -> Bool
  Requires: 
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True
  
  Examples:
     valid_bid([],Bid("pass", None)) => True
     valid_bid([Bid("pass", None), Bid("pass", None), 
                 Bid("pass", None)], Bid("pass", None)) 
                  => True 
     valid_bid([Bid("1", "C"), Bid("pass", None), 
                 Bid("pass", None), Bid("pass", None)], 
                  Bid("pass", None)) => False
     valid_bid([Bid("7", "NT")], Bid("2", "H")) => False
     valid_bid([Bid("1", "C"), Bid("pass", None)], 
                 Bid("double", None)) => False
     valid_bid([Bid("1", "C"), Bid("pass", None), 
                 Bid("pass", None)], Bid("double", None)) 
                   => True
  '''
  def valid_numeric(L, v):
    if L == [Bid('pass', None)]*3:
      return True
    else:
      for i in range(len(L)-1):
        if L[i].value.isdigit():
          return v > L[i]
      return False
  
  def valid_double(L):
    idx = 0
    for i in range(len(L)-1):
      if L[i].value == 'pass' and L[i+1].value == 'pass':
        idx += 1
      elif i == 0 and L[i].value != 'pass':
        return True
      elif idx%2 == 0:
        return False
      else:
        return True
      
  def valid_redouble(L):
    idx = 0
    for i in range(len(L)-1):
      if L[i].value == 'pass' and L[i+1].value == 'pass':
        idx += 1
      elif L[i].value == 'double':
        return idx%2 == 1
      else:
        return False
  
  val = new_bid.value
  if val == 'pass':
    if len(bids) == 3 and bids == [Bid('pass', None)]*3:
      return True
    # cannot pass with already 3 passes
    else:
      return not bids[-3:] == [Bid('pass', None)]*3
  elif val.isdigit():
    # numeric bid must be larger than previous
    return valid_numeric(bids[::-1], new_bid)
  elif val == 'double':
    # last non-pass bid must be from opposing team
    if not bids:
      return False
    else:
      return valid_double(bids[::-1])
  elif val == 'redouble':
    if not bids:
      return False
    else:
      return valid_redouble(bids[::-1])


def bidding_complete(bids):
  '''
  Returns True if bids represents a complete contract and False otherwise
  
  bidding_complete: (listof Bid) -> Bool
  Requires: 
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True 
  
  Examples:
     bidding_complete([Bid("pass", None), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => True
     bidding_complete([Bid("1", "C"), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => True
     bidding_complete([Bid("1", "C"), Bid("3", "NT"), 
                Bid("pass", None), Bid("pass", None)]) => False
  '''
  def valid_completion(L):
    for i in range(len(L)):
      if L[i].value.isdigit():
        return True
    return False
  
  if len(bids) < 4 or bids[-3:] != [Bid('pass', None)]*3:
    return False
  elif bids == [Bid('pass', None)]*4:
    return True
  else:
    if bids[-4].value.isdigit():
        return True
    else:
      valid_completion(bids[:-4][::-1])

  
def contract(bids):
  '''
  Returns the contract to be played, including any doubling 
  or redoubling that occurred.
  
  contract: (listof Bid) -> (list Bid (anyof Bid None))
  Requires: 
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True 
     bidding_complete(bids) => True
  
  Examples:
     contract([Bid("pass", None), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)])
                  => [Bid("pass", None), None]
     contract([Bid("1", "C"), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) 
                  => [Bid("1", "C"), None]
     contract([Bid("1", "C"), Bid("double", None), 
                Bid("pass", None), Bid("pass", None), 
                Bid("pass", None)]) 
                  => [Bid("1", "C"), Bid("double", None)]
     contract([Bid("1", "C"), Bid("double", None), 
                Bid("redouble", None), Bid("pass", None),
                Bid("pass", None),  Bid("pass", None)]) 
                 => [Bid("1", "C"), Bid("redouble", None)]
     contract([Bid("1", "C"), Bid("double", None), 
                Bid("redouble", None), Bid("1", "S"), 
                Bid("pass", None), Bid("pass", None), 
                Bid("pass", None)]) => [Bid("1", "S"), None]
  '''
  final_contract = []
  m = final_contract
  L = bids[::-1]
  if bids == [Bid('pass', None)]*4:
    return [Bid('pass', None), None]
  for k in range(len(L)):
    if L[k].value == 'redouble' or L[k].value == 'double':
      final_contract.append(L[k])
    if L[k].value.isdigit():
      final_contract.append(L[k])
      if final_contract[0].value == 'redouble':
        if Bid('double', None) in final_contract:
          m.remove(Bid('double', None))
        return final_contract[::-1]
      elif final_contract[0].value == 'double':
        if Bid('redouble', None) in final_contract:
          m.remove(Bid('redouble', None))
        return final_contract[::-1]
      else:
        return final_contract[::-1] + [None]


##PROVIDED FUNCTIONS BELOW - DO NOT CHANGE
  
def declarer(starting_team, bids):
  '''
  Returns who the declarer is given the starting_team
  and the bids. Returns None if all passed contract.
  
  declarer: Str (listof Bid) -> (anyof Str None)
  Requires:
     starting_team is one of "North", "East", "South" or "West"
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True 
     bidding_complete(bids) => True
     
  Examples:
     declarer("North", [Bid("pass", None), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => None
     declarer("North", [Bid("1", "C"), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => "North" 
     declarer("North", [Bid("1", "C"), Bid("2", "C"),
                Bid("3", "C"), Bid("pass", None),
                Bid("pass", None), Bid("pass", None)]) => "North"
  '''
  all_pass = [Bid("pass", None)]*4
  if all_pass == bids:
    return None
  deal_contract = contract(bids)
  players = ["North", "East", "South", "West"]
  winning_team = None
  cur_dir = starting_team
  for i in bids:
    if i == deal_contract[0]:
      winning_team = cur_dir
    cur_dir = players[(players.index(cur_dir) + 1) % len(players)]
    
  winning_team = [winning_team, 
                  players[(players.index(winning_team) + 2) % len(players)]]
  cur_dir = starting_team
  for i in bids:
    if i.suit == deal_contract[0].suit and cur_dir in winning_team:
      return cur_dir
    cur_dir = players[(players.index(cur_dir) + 1) % len(players)]



def bidding_bootstrap(deck = []):
  '''
  Performs a deal and bidding sequence for Bridge.
  Bids should be made of the format #S, pass, double or redouble 
  where # is a number from 1 to 7 and S is a suit C, D, H, S, NT.
  
  bidding_bootstrap: [(listof Nat)] -> (list Player Player Player Player)
  Requires:
     1 <= deck[i] <= 52 for all indices i.
  '''

  players = deal_bootstrap(deck) #From a10q1
  invalid_response = "Invalid response."
  invalid_bid_response = "Invalid bid."
  bid_prompt = "Please enter a valid bid for {0}: "
  odd_bids = ['pass', 'double', 'redouble']   
  bids = []
  num_players = len(players)
  starting_player = num_players - 1
  while not bidding_complete(bids):
    print("{0}'s hand: ".format(players[starting_player].name))
    display_hand(players[starting_player].hand)
    bid = input(bid_prompt.format(players[starting_player].name))
    
    def good_bid_input(bid):
      '''
      Local helper function to determine a good bid
    
      good_bid_input: Str -> Bool
      '''      
      num = bid[0]
      suit = bid[1:]
      if bid in odd_bids:
        return True
      elif num not in ['1', '2', '3', '4', '5', '6', '7'] or \
        suit not in SUITS:
        return False
      return True
    
    while not good_bid_input(bid):
      print(invalid_response)
      print("{0}'s hand: ".format(players[starting_player].name))
      display_hand(players[starting_player].hand)
      bid = input(bid_prompt.format(players[starting_player].name))  
    if bid in odd_bids:
      bid = Bid(bid, None)
    else:
      num = bid[0]
      suit = bid[1:]      
      bid = Bid(num, suit)
    if not valid_bid(bids, bid):
      print(invalid_bid_response)
    else:
      bids.append(bid)
      starting_player = (starting_player + 1) % num_players
  return [players, bids]

## Examples for __eq__
c = Bid("1", "C")
d = Bid("1", "D")
e = Bid("1", "C")
f = Bid("pass", None)
check.expect("Test unequal", c == d, False)
check.expect("Test equal", c == e, True)
check.expect("Test against pass", c == f, False)

## Examples for __lt__
check.expect("Test lt true", c < d, True)
check.expect("Test lt false", c < e, False)
check.expect("Test lt pass", c < f, False)

## Examples for Valid Bid

check.expect("Test on empty", valid_bid([],Bid("pass", None)), True)
check.expect("Test on empty double", valid_bid([],Bid("double", None)), False)
check.expect("Test on empty redouble", 
             valid_bid([],Bid("redouble", None)), False)
check.expect("Test all pass", 
             valid_bid([Bid("pass", None), Bid("pass", None), 
                        Bid("pass", None)], Bid("pass", None)), True)
check.expect("Test passes after bid",
             valid_bid([Bid("1", "C"), Bid("pass", None), 
                        Bid("pass", None), Bid("pass", None)], 
                        Bid("pass", None)), False)
check.expect("Test bid after max", valid_bid([Bid("7", "NT")],
                                              Bid("2", "H")), False)
check.expect("Test invalid double", 
             valid_bid([Bid("1", "C"), Bid("pass", None)], 
                       Bid("double", None)), False)
check.expect("Test valid double", 
valid_bid([Bid("1", "C"), Bid("pass", None), Bid("pass", None)], 
          Bid("double", None)), True)
          
## Examples contract

check.expect("Test all pass", 
             contract([Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None), Bid("pass", None)]),
            [Bid("pass", None), None])


check.expect("Test simple contract", 
             contract([Bid("1", "C"), Bid("pass", None), 
           Bid("pass", None), Bid("pass", None)]) ,
             [Bid("1", "C"), None])

check.expect("Test simple doubled", 
             contract([Bid("1", "C"), Bid("double", None), 
                       Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None)]) ,
             [Bid("1", "C"), Bid("double", None)])

check.expect("Test simple redoubled", 
             contract([Bid("1", "C"), Bid("double", None), 
                       Bid("redouble", None), Bid("pass", None),
                       Bid("pass", None),  Bid("pass", None)]) ,
             [Bid("1", "C"), Bid("redouble", None)])

check.expect("Test simple redoubled rebid", 
             contract([Bid("1", "C"), Bid("double", None), 
                       Bid("redouble", None), Bid("1", "S"), 
                       Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None)]),
             [Bid("1", "S"), None])
             
## Examples Declarer

check.expect("Test all pass", 
             declarer("North",
                      [Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None), Bid("pass", None)]),
             None)

check.expect("Test Simple 1C", 
declarer("North", [Bid("1", "C"), Bid("pass", None), 
           Bid("pass", None), Bid("pass", None)]), "North")

check.expect("Test Simple 3C", 
declarer("North", [Bid("1", "C"), Bid("2", "C"),
           Bid("3", "C"), Bid("pass", None),
           Bid("pass", None), Bid("pass", None)]), "North")

## Examples bidding_complete

check.expect("Example empty", bidding_complete([]), False)
check.expect("Example all-pass",
             bidding_complete([Bid("pass", None), Bid("pass", None), 
                               Bid("pass", None), Bid("pass", None)]), True)
check.expect("Example bid three pass", 
             bidding_complete([Bid("1", "C"), Bid("pass", None), 
                               Bid("pass", None), Bid("pass", None)]), True)
check.expect("Example incomplete", 
             bidding_complete([Bid("1", "C"), Bid("3", "NT"), 
                        Bid("pass", None), Bid("pass", None)]), False)