package org.example.demo;

import jade.core.Agent;
import jade.core.behaviours.*;
import jade.core.AID;
import jade.lang.acl.ACLMessage;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.wrapper.AgentController;
import jade.wrapper.ContainerController;
import jade.core.Runtime;
import jade.core.Profile;
import jade.core.ProfileImpl;

import java.util.*;

//----------------------------------------
// Shared Data Models
//----------------------------------------
class StockMarket {
    static Map<String, Double> stockPrices = new HashMap<>();
    static Map<String, List<Double>> priceHistory = new HashMap<>();
    static Map<String, List<String>> tradeHistory = new HashMap<>();
    static Map<String, List<Integer>> tradeCountHistory = new HashMap<>();
    static Map<String, List<Double>> tradeTimePoints = new HashMap<>();
    static Map<String, List<Double>> timePoints = new HashMap<>();
    static final double MIN_PRICE = 1.0;
    static final int MAX_HISTORY = 50;
    static long startTime = System.currentTimeMillis();

    static void adjustPrice(String company, double newPrice) {
        newPrice = Math.max(newPrice, MIN_PRICE);
        stockPrices.put(company, newPrice);
        
        List<Double> prices = priceHistory.get(company);
        List<Double> times = timePoints.get(company);
        double timePoint = (System.currentTimeMillis() - startTime) / 1000.0;
        
        prices.add(newPrice);
        times.add(timePoint);
        
        if (prices.size() > MAX_HISTORY) {
            prices.remove(0);
            times.remove(0);
        }
    }

    static void initStocks(List<String> companies, double initialPrice) {
        startTime = System.currentTimeMillis();
        for (String c : companies) {
            stockPrices.put(c, initialPrice);
            priceHistory.put(c, new ArrayList<>(List.of(initialPrice)));
            timePoints.put(c, new ArrayList<>(List.of(0.0)));
            tradeHistory.put(c, new ArrayList<>());
            tradeTimePoints.put(c, new ArrayList<>(List.of(0.0)));
            tradeCountHistory.put(c, new ArrayList<>(List.of(0)));
        }
    }
    static void recordTrade(String company, String trade) {
        // Record the trade
        List<String> trades = tradeHistory.get(company);
        trades.add(trade);
        
        // Update trade count history with cumulative count for this time period
        List<Integer> countHistory = tradeCountHistory.get(company);
        List<Double> times = tradeTimePoints.get(company);
        double timePoint = (System.currentTimeMillis() - startTime) / 1000.0;
        
        // If we're in a new time period, add a new count
        if (times.isEmpty() || timePoint > times.get(times.size() - 1)) {
            countHistory.add(trades.size());
            times.add(timePoint);
        } else {
            // Update the count for the current time period
            countHistory.set(countHistory.size() - 1, trades.size());
        }
        
        // Keep histories in sync and within MAX_HISTORY limit
        while (countHistory.size() > MAX_HISTORY) {
            countHistory.remove(0);
            times.remove(0);
            if (!trades.isEmpty()) {
                trades.remove(0);
            }
        }
    }
}


