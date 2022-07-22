import logging
from zerodha import getKite
from instruments import fetchInstruments
from quotes import getCMP
from orders import placeOrder, modifyOrder, placeSLOrder, cancelOrder
from utils import roundToNSEPrice
from RSI_Strategy import RSI
import time

def startAlgo():
  logging.info("Algo started...")
  rsi_data = RSI()
  size = rsi_data.size
  previous_day_rsi = rsi_data[size - 1]
  if(previous_day_rsi > 30 and previous_day_rsi < 50) : 
    return
  if(previous_day_rsi < 30) :
    logging.info("Oversold Correct Time to Buy")
  if(previous_day_rsi > 50) :
    logging.info("RSI Trending UP")
  direction = 'LONG'
  kite = getKite()
  fetchInstruments(kite)

  exchange = 'NSE';
  tradingSymbol = 'RELIANCE'
  lastTradedPrice = getCMP(exchange + ':' + tradingSymbol)
  logging.info(tradingSymbol + ' CMP = %f', lastTradedPrice)

  limitPrice = lastTradedPrice - lastTradedPrice * 1 / 100
  limitPrice = roundToNSEPrice(limitPrice)
  qty = 1
  direction = 'LONG'

  # place order
  origOrderId = placeOrder(tradingSymbol, limitPrice, qty, direction)
  logging.info('Original order Id %s', origOrderId)

  # sleep for 10 seconds then modify order
  time.sleep(10)
  newPrice = lastTradedPrice
  modifyOrder(origOrderId, newPrice)

  # sleep for 10 seconds and then place SL order
  time.sleep(10)
  slPrice = newPrice - newPrice * 1 / 100
  slPrice = roundToNSEPrice(slPrice)
  slDirection = 'SHORT' if direction == 'LONG' else 'LONG'
  slOrderId = placeSLOrder(tradingSymbol, slPrice, qty, slDirection)
  logging.info('SL order Id %s', slOrderId)

  # sleep for 10 seconds and then place target order
  time.sleep(10)
  targetPrice = newPrice + newPrice * 2 / 100
  targetPrice = roundToNSEPrice(targetPrice)
  targetDirection = 'SHORT' if direction == 'LONG' else 'LONG'
  targetOrderId = placeOrder(tradingSymbol, targetPrice, qty, targetDirection)
  logging.info('Target order Id %s', targetOrderId)

  # sleep for 10 seconds and cancel target order
  time.sleep(10)
  cancelOrder(targetOrderId)
  logging.info('Cancelled Target order Id %s', targetOrderId)

  logging.info("Algo done executing all orders. Check ur orders and positions in broker terminal.")


