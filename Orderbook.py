
import time
import random
import pandas as pd

UNIX_TIME = round(int(time.time()) / 1000,0)


class Orderbook:
  def __init__(self):
    self.order_list = []
    self.ask_side = []
    self.bid_side = []
    self.trades = []

  def add_new_order(self,new_order):
    self.order_list.append(new_order)
    if new_order['SIDE'] == 'BIDS':
      self.bid_side.append(new_order)
      self.orderbook()
      self.bid_trades(new_order)
      self.orderbook()     
    else:
      self.ask_side.append(new_order)
      self.orderbook()
      self.ask_trades(new_order)
      self.orderbook()
    
    return self.orderbook()[0], self.trades
  
  def orderbook_initializer(self,depth=5,initial_price=10,tick_size=0.1,initial_agent_wealth=100):
    bid_initial_price = initial_price
    ask_initial_price = initial_price + tick_size
    if len(self.bid_side) == 0:
      while len(self.bid_side) < depth:
        MAX_BID_QUANTITY = initial_agent_wealth / initial_price
        MAX_ASK_QUANTITY = initial_agent_wealth / (initial_price + (depth*tick_size))
        RANDOM_BID_QUANTITY = round(random.uniform(1, MAX_BID_QUANTITY),2)
        RANDOM_ASK_QUANTITY = round(random.uniform(1,MAX_ASK_QUANTITY),2)
        initial_bid_order = {'PRICE': bid_initial_price, 'QUANTITY':RANDOM_BID_QUANTITY,'TIME':UNIX_TIME, 'SIDE':'BIDS', 'TYPE':'LIMIT'}
        initial_ask_order = {'PRICE': ask_initial_price, 'QUANTITY':RANDOM_ASK_QUANTITY,'TIME':UNIX_TIME, 'SIDE':'ASKS', 'TYPE':'LIMIT'}
        self.bid_side.append(initial_bid_order)
        self.ask_side.append(initial_ask_order)
        self.order_list.append(initial_bid_order)
        self.order_list.append(initial_ask_order)
        bid_initial_price -= tick_size
        ask_initial_price += tick_size
        continue
    return self.order_list

  def orderbook(self):
    bid_ordered_book = sorted(self.bid_side, key=lambda x:(x['PRICE'], x['TIME']), reverse=True)
    ask_ordered_book = sorted(self.ask_side, key=lambda x:(x['PRICE'], x['TIME']))
    for order in bid_ordered_book:
      order['PRICE'] = round(order['PRICE'], 2)
        
    for order in ask_ordered_book:
      order['PRICE'] = round(order['PRICE'],2) 
    
    orderbook = {'BIDS':bid_ordered_book, 'ASKS':ask_ordered_book}
    return orderbook, bid_ordered_book, ask_ordered_book

  def orderbook_manager(self):
    bid_orderbook = self.orderbook()[1] #for easy naming purpose
    ask_orderbook = self.orderbook()[2] #for easy naming purpose
    best_bid_price = 0
    best_bid_quantity = 0
    best_ask_price = 0
    best_ask_quantity = 0
    if len(bid_orderbook) == 0:
      best_bid_price = 0
      best_ask_quantity = 0
    else:
      best_bid_price = bid_orderbook[0]['PRICE']
      best_bid_quantity = bid_orderbook[0]['QUANTITY']
    if len(ask_orderbook) == 0:
      best_ask_price = 0
      best_ask_quantity = 0
    else:
      best_ask_price = ask_orderbook[0]['PRICE']
      best_ask_quantity = ask_orderbook[0]['QUANTITY']
        
    midprice = (best_ask_price + best_bid_price)/2
    return best_bid_price, best_bid_quantity, best_ask_price, best_ask_quantity, midprice

  def get_best_bid(self):
    return self.orderbook_manager()[0]
  def get_best_bid_quantity(self):
    return self.orderbook_manager()[1]
  def get_best_ask(self):
    return self.orderbook_manager()[2]
  def get_best_ask_quantity(self):
    return self.orderbook_manager()[3]
  def get_midprice(self):
    return self.orderbook_manager()[4]
  def get_trades(self):
    return self.add_new_order(new_order)[1]
  
  def bid_trades(self,new_order):
    trade_occur = False
    bid_side_book = self.orderbook()[1]
    ask_side_book = self.orderbook()[2]
    if new_order['SIDE'] == 'BIDS' and new_order['TYPE'] == 'LIMIT':
      if new_order['PRICE'] >= ask_side_book[0]['PRICE']: #IF TRADE OCCURS
          trade_occur = True
          if new_order['QUANTITY'] >= ask_side_book[0]['QUANTITY']: 
              remained_quantity = new_order['QUANTITY'] - ask_side_book[0]['QUANTITY']
              new_order['QUANTITY'] = remained_quantity
              trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':ask_side_book[0]['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':True}
              self.trades.append(trade)             
              del(ask_side_book[0]) #remove the best_ask from the ask_side_book
              while remained_quantity > 0: 
                new_order['QUANTITY'] = remained_quantity
                if new_order['PRICE'] >= ask_side_book[0]['PRICE']:                                   
                  if new_order['QUANTITY'] >= ask_side_book[0]['QUANTITY']: #CHECK THE QUANITTY OF THE REMAINED 
                    remained_quantity =  new_order['QUANTITY'] - ask_side_book[0]['QUANTITY'] 
                    new_order['QUANTITY'] = remained_quantity
                    self.bid_side.append(new_order)
                    trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':ask_side_book[0]['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':True}
                    self.trades.append(trade)                                              
                    del(ask_side_book[0])               
                    #maybe should break then return everything at the end if the code does not work                    
                  else:
                    remained_quantity =  ask_side_book[0]['QUANTITY'] - new_order['QUANTITY']
                    ask_side_book[0]['QUANTITY'] = remained_quantity
                    trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':new_order['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':True}
                    self.trades.append(trade)                    
                    break                         
                else: #TRADE DID NOT OCCUR ANYMORE AS THE NEXT BEST ASK IS NOT THE SAME PRICE OR LOWER THAN THE BID
                  self.bid_side.append(new_order)
                  return self.bid_side 
          else:
              remained_quantity = ask_side_book[0]['QUANTITY'] - new_order['QUANTITY']
              ask_side_book[0]['QUANTITY'] = remained_quantity
              trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':new_order['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':True}      
              self.trades.append(trade)
      else:
        self.bid_side.append(new_order)
        #trade did not occur so add new order to the bid_side
        return bid_side_book 
    

  def ask_trades(self,new_order):
    trade_occur = False
    bid_side_book = self.orderbook()[1]
    ask_side_book = self.orderbook()[2]
    if new_order['SIDE'] == 'ASKS' and new_order['TYPE'] == 'LIMIT':
      if new_order['PRICE'] <= self.bid_side[0]['PRICE']:
        trade_occur = True
        if new_order['QUANTITY'] >= self.bid_side[0]['QUANTITY']:
            remained_quantity = new_order['QUANTITY'] - self.bid_side[0]['QUANTITY']
            new_order['QUANTITY'] = remained_quantity
            trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':self.bid_side[0]['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':True}
            self.trades.append(trade)      
            del(self.bid_side[0])
            while remained_quantity > 0:
                if new_order['PRICE'] >= self.bid_side[0]['PRICE']:
                    remained_quantity = new_order['QUANTITY'] - self.bid_side[0]['QUANTITY']             
                    if new_order['QUANTITY'] >= self.bid_side[0]['QUANTITY']:
                        remained_quantity =  new_order['QUANTITY'] - self.bid_side[0]['QUANTITY'] 
                        new_order['QUANTITY'] = remained_quantity
                        self.ask_side.append(new_order)
                        trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':self.bid_side[0]['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':False}
                        self.trades.append(trade)
                        print('TRADE:',trade)
                        print('ASK LIST', self.ask_side)
                        del(self.bid_side[0])
                        print('IF BID_LIST:', self.bid_side)
                        break
                    else:
                        remained_quantity =  self.bid_side[0]['QUANTITY'] - new_order['QUANTITY']
                        self.bid_side[0]['QUANTITY'] = remained_quantity
                        trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':new_order['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':False}
                        self.trades.append(trade)                                       
                        break                           
                else:
                    self.ask_side.append(new_order)
                                                              
        else:
          remained_quantity = self.bid_side[0]['QUANTITY'] - new_order['QUANTITY']
          self.bid_side[0]['QUANTITY'] = remained_quantity
          trade = {'PRICE:':new_order['PRICE'], 'QUANTITY:':new_order['QUANTITY'],'TIME:':UNIX_TIME, 'isMaker:':True}
          self.trades.append(trade)
          
    else:
      self.ask_side.append(new_order)
    print(self.trades, trade_occur)  
      

class Agent(Orderbook):
    def __init__(self):
        self.midprice = Orderbook().get_midprice()
        self.best_bid = Orderbook().get_best_bid()
        self.best_bid_quantity = Orderbook().get_best_bid_quantity()
        self.best_ask = Orderbook().get_best_ask()
        self.best_qsk_quantity = Orderbook().get_best_ask_quantity()
        
    def create_random_agent(self, wealth):
        self.wealth = wealth
        order_type = 'LIMIT'
        open_position = 0
        MIN_QUANTITY = 0.1
        MAX_QUANTITY = wealth/(self.best_ask + MIN_QUANTITY) #to avoid division 0 error
        random_position = 'BIDS'
        random_side = random.randint(0,1)
        random_bid_ask = round(random.uniform(self.best_bid, self.best_ask),2)
        
        random_quantity = round(random.uniform(0.1,MAX_QUANTITY),2)
        
        if random_side == 1:
            random_position = 'ASKS'
    
        if self.wealth > self.best_bid and open_position < 5:
            order ={'PRICE':random_bid_ask,'QUANTITY':random_quantity,'TIME':UNIX_TIME,'SIDE':random_position,'TYPE':order_type}
            open_position += 1
            return order 



def tester():
  OB = Orderbook()
  OB.orderbook_initializer()
  new_order = {'PRICE': 10.1, 'QUANTITY': 2, 'TIME': 1676106.0, 'SIDE': 'BIDS', 'TYPE': 'LIMIT'}
  OB.add_new_order(new_order)
  print(OB.orderbook()[0])
  print(f'BEST_BID:{OB.get_best_bid()},\nBEST_BID_QUANTITY:{OB.get_best_bid_quantity()}, \nBEST_ASK:{OB.get_best_ask()}, \nBEST_ASK_QUANTITY:{OB.get_best_ask_quantity()}')
  print('TRADES:', OB.get_trades())

if __name__ == "__main__":
  tester()

  
