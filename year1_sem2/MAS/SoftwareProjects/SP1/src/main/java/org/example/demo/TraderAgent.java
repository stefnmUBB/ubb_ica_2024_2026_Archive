package org.example.demo;

import jade.core.Agent;

import java.util.HashMap;
import java.util.Map;

//----------------------------------------
// Abstract Trader Agent
//----------------------------------------
abstract class TraderAgent extends Agent {
    protected double capital;
    protected Map<String, Integer> portfolio = new HashMap<>();

    protected void buy(String company, int amount) {
        double price = StockMarket.stockPrices.get(company);
        double cost = amount * price;
        if (capital >= cost) {
            capital -= cost;
            portfolio.put(company, portfolio.getOrDefault(company, 0) + amount);
            StockMarket.recordTrade(company, getLocalName() + " BUY " + amount);
        }
    }

    protected void sell(String company, int amount) {
        int held = portfolio.getOrDefault(company, 0);
        if (held >= amount) {
            double price = StockMarket.stockPrices.get(company);
            capital += amount * price;
            portfolio.put(company, held - amount);
            StockMarket.recordTrade(company, getLocalName() + " SELL " + amount);
        }
    }
}

