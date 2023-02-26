class Agent(Orderbook):
  def __init__(self):
    super().__init__()
    Orderbook.orderbook_initializer(self)
    Orderbook.get_orderbook(self)
    self.midprice = Orderbook.get_midprice(self)
    self.best_ask = Orderbook.get_best_ask(self)
    self.best_bid = Orderbook.get_best_bid(self)
    self.best_bid_quantity = Orderbook.get_best_bid_quantity(self)
    self.best_ask_quantity = Orderbook.get_best_ask_quantity(self)
    self.tick_size = 1
  
  def random_agent(self,wealth=100):
    side =  'BIDS'
    range = 0.2
    MAX_BID = self.best_bid * (1-range)
    MAX_ASK = self.best_ask * (1+range)
    MAX_BID_QUANTITY = wealth/self.best_bid
    MAX_ASK_QUANTITY = wealth/self.best_ask
    random_ask_quantity= round(random.uniform(1,MAX_ASK_QUANTITY),2)
    random_bid_quantity = round(random.uniform(1,MAX_BID_QUANTITY),2)
    random_bid = round(random.uniform(MAX_BID, self.best_ask),2)
    random_ask = round(random.uniform(self.best_bid,MAX_ASK),2)
    bid_price = self.best_bid
    ask_price = self.best_ask
    quantity = random.randint(1,10)
    order = {'PRICE': random_bid, 'QUANTITY': random_bid_quantity, 'TIME':UNIX_TIME, 'SIDE':side,'TYPE':'LIMIT'}
    random_side = random.randint(0,1)
    if random_side == 1:
      side = 'ASKS'
      order = {'PRICE': random_ask, 'QUANTITY': random_ask_quantity, 'TIME':UNIX_TIME, 'SIDE':side,'TYPE':'LIMIT'}

    return order

def main_agent():
  OB = Orderbook()
  agent = Agent()
  OB.orderbook_initializer()
  i = 0
  while i < 10:
    print(f'ORDERBOOK BEFORE TRADE: {OB.get_orderbook()}')
    new_order = agent.random_agent() 
    OB.add_new_order(new_order)
    print(f'TRADE:{OB.get_trades()}')
    print(f'Orderbook after trade: {OB.get_orderbook()}')
    print('-----------------------------------------------')
    i +=1
    continue
  
  

if __name__ == "__main__":
  main_agent()
