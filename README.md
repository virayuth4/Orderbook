# Orderbook
Orderbook in Python 

This is a project to simulate a Limit Orderbook (LOB) that I made. 

An orderbook is a book that contains the BIDS and the ASKS price of a given asset (i.e APPL). Bids are sorted from high to low, while asks are sorted from low to high. 

![orderbook](https://user-images.githubusercontent.com/101397910/218970924-589bbd6d-80b0-425c-bc77-80d7303cf655.png)

(IMG Source: https://www.quantstart.com/articles/high-frequency-trading-ii-limit-order-book/)

A trade occurs by either a submission of a limit order to buy at the best asks price or a sell at the best bids price. Or a market order where the buyer/seller
executes the trade immediately at the best bid or best ask price. In this first iteration of the orderbook, only LIMIT order is available.

I plan to upgrade this project by including different type of orders, cancellation of orders, and also agents to simulate actual trading activities. 
