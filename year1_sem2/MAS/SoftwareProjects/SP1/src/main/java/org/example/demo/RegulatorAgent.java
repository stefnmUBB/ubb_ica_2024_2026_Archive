package org.example.demo;

import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour;

//----------------------------------------
// Regulator Agent
//----------------------------------------
public class RegulatorAgent extends Agent {
    protected void setup() {
        addBehaviour(new TickerBehaviour(this, 3000) {
            protected void onTick() {
                for (String c : StockMarket.stockPrices.keySet()) {
                    int trades = StockMarket.tradeHistory.get(c).size();
                    double price = StockMarket.stockPrices.get(c);
                    double newPrice = price + (trades * 0.5 - 1);
                    StockMarket.adjustPrice(c, newPrice);
                }
            }
        });
    }
}
