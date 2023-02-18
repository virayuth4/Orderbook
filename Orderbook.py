import math
import random
import time
UNIX_TIME = math.ceil(int(time.time()))

class Orderbook:
  def __init__(self):
    self.UNIX_TIME = math.ceil(int(time.time()))
    self.order_list = []
    self.ask_side = []
    self.bid_side = []
    self.trades = []
  
  def orderbook_initializer(self,depth=5,initial_price=10,tick_size=0.1,initial_agent_wealth=100):
    bid_initial_price = initial_price
    ask_initial_price = initial_price + tick_size
    if len(self.bid_side) == 0:
      while len(self.bid_side) < depth:
        MAX_BID_QUANTITY = initial_agent_wealth / initial_price
        MAX_ASK_QUANTITY = initial_agent_wealth / (initial_price + (depth*tick_size))
        RANDOM_BID_QUANTITY = round(random.uniform(1, MAX_BID_QUANTITY),2)
        RANDOM_ASK_QUANTITY = round(random.uniform(1,MAX_ASK_QUANTITY),2)
        initial_bid_order = {'PRICE': bid_initial_price, 'QUANTITY':RANDOM_BID_QUANTITY,'TIME':self.UNIX_TIME, 'SIDE':'BIDS', 'TYPE':'LIMIT'}
        initial_ask_order = {'PRICE': ask_initial_price, 'QUANTITY':RANDOM_ASK_QUANTITY,'TIME':self.UNIX_TIME, 'SIDE':'ASKS', 'TYPE':'LIMIT'}
        self.bid_side.append(initial_bid_order)
        self.ask_side.append(initial_ask_order)
        self.order_list.append(initial_bid_order)
        self.order_list.append(initial_ask_order)
        bid_initial_price -= tick_size
        ask_initial_price += tick_size
        continue
    return self.order_list

  def add_new_order(self, new_order):
    if new_order['SIDE'] == 'BIDS' and new_order['TYPE'] == 'LIMIT':
      self.bid_side.append(new_order)
      self.book_organizer()
      self.check_bid_trade(new_order)
    else:
      self.ask_side.append(new_order)
      self.book_organizer()
      self.check_ask_trade(new_order)

  def book_organizer(self):
    self.bid_side = sorted(self.bid_side, key=lambda x:(x['PRICE'], -x['TIME']), reverse=True) #updated sorting as it was wrong before 
    self.ask_side  = sorted(self.ask_side, key=lambda x:(x['PRICE'], x['TIME']))
    for order in self.bid_side:
      order['PRICE'] = round(order['PRICE'], 2)
      order['QUANTITY'] = round(order['QUANTITY'],2)    
    for order in self.ask_side:
      order['PRICE'] = round(order['PRICE'],2) 
      order['QUANTITY'] = round(order['QUANTITY'],2)
    
  def check_bid_trade(self, new_order):
    if new_order['PRICE'] >= self.ask_side[0]['PRICE']:
      if new_order['QUANTITY'] >= self.ask_side[0]['QUANTITY']:
        new_order['QUANTITY'] -= self.ask_side[0]['QUANTITY']
        trade = {'PRICE:':self.ask_side[0]['PRICE'], 'QUANTITY:':self.ask_side[0]['QUANTITY'],'TIME:':self.UNIX_TIME, 'isMaker:':True}
        self.trades.append(trade)
        del(self.ask_side[0]) 
        while new_order['QUANTITY'] > 0:
          if new_order['PRICE'] >= self.ask_side[0]['PRICE']:  
            if new_order['QUANTITY'] >= self.ask_side[0]['PRICE']:
              new_order['QUANTITY'] -= self.ask_side[0]['QUANTITY']
              trade = {'PRICE:':self.ask_side[0]['PRICE'], 'QUANTITY:':self.ask_side[0]['QUANTITY'],'TIME:':self.UNIX_TIME, 'isMaker:':True} 
              self.trades.append(trade)
              del(self.ask_side[0])
            else:
              self.ask_side[0]['QUANTITY'] -= new_order['QUANTITY']
          else:
            return
      else:
        self.ask_side[0]['QUANTITY'] -= new_order['QUANTITY']
    else:
      return
    return self.trades, self.bid_side, self.ask_side  

  def check_ask_trade(self, new_order):
    if new_order['PRICE'] <= self.bid_side[0]['PRICE']:
      if new_order['QUANTITY'] >= self.bid_side[0]['QUANTITY']:
        new_order['QUANTITY'] -= self.bid_side[0]['QUANTITY']
        trade = {'PRICE:':self.bid_side[0]['PRICE'], 'QUANTITY:':self.bid_side[0]['QUANTITY'],'TIME:':self.UNIX_TIME, 'isMaker:':True}
        self.trades.append(trade)
        del(self.bid_side[0])
        while new_order['QUANTITY'] > 0:
          if new_order['PRICE'] <= self.bid_side[0]['PRICE']:
            if new_order['QUANTITY'] >= self.bid_side[0]['PRICE']:
              new_order['QUANTITY'] -= self.bid_side[0]['QUANTITY']
              trade = {'PRICE:':self.bid_side[0]['PRICE'], 'QUANTITY:':self.bid_side[0]['QUANTITY'],'TIME:':self.UNIX_TIME, 'isMaker:':True} 
              self.trades.append(trade)
              del(self.bid_side[0])
            else:
              self.bid_side[0]['QUANTITY'] -= new_order['QUANTITY']
          else:
            return
      else:
        self.bid_side[0]['QUANTITY'] -= new_order['QUANTITY']
    else:
      return
    return self.trades, self.bid_side, self.ask_side

  def get_trades(self):
    return self.trades
  def get_orderbook(self):
    orderbook = {'BIDS': self.bid_side, 'ASKS':self.ask_side}
    return orderbook
  def get_midprice(self):
    return (self.bid_side[0]['PRICE'] + self.ask_side[0]['PRICE'])/2
  def get_best_bid(self):
    return self.bid_side[0]['PRICE']
  def get_best_bid_quantity(self):
    return self.bid_side[0]['QUANTITY']
  def get_best_ask(self):
    return self.ask_side[0]['PRICE']
  def get_best_ask_quantity(self):
    return self.ask_side[0]['QUANTITY']
 


def main():
  OB = Orderbook()
  OB.orderbook_initializer()
  #new_order = {'PRICE': 10, 'QUANTITY': 10, 'TIME': UNIX_TIME-1, 'SIDE': 'ASKS', 'TYPE': 'LIMIT'} 
  new_order = {'PRICE': 10.1, 'QUANTITY': 10, 'TIME': UNIX_TIME-1, 'SIDE': 'BIDS', 'TYPE': 'LIMIT'} 
  OB.add_new_order(new_order)
  print('TRADE:',OB.get_trades())
  print(OB.get_orderbook())
  print(OB.get_midprice())

  

if __name__ == "__main__":
  main()
  
