package org.example.demo;

import jade.core.behaviours.TickerBehaviour;

import java.util.List;

//----------------------------------------
// Trend Trader Agent
//----------------------------------------
public class TrendTraderAgent extends TraderAgent {
    private String targetCompany;
    private int k;
    private double threshold;

    protected void setup() {
        capital = 10000.0;
        k = 3;
        threshold = 5.0;
        //targetCompany = "C1"; // example

        addBehaviour(new TickerBehaviour(this, 1000) {
            protected void onTick() {
                targetCompany = Math.random()<0.5 ? "C1":"C2";

                if(Math.random()<0.1) {
                    if(Math.random()<0.5)
                        buy(targetCompany, 1);
                    else
                        sell(targetCompany, 1);
                    return;
                }

                List<Double> history = StockMarket.priceHistory.get(targetCompany);
                if (history.size() >= k) {
                    double delta = history.get(history.size() - 1) - history.get(history.size() - k);
                    if (delta > threshold) sell(targetCompany, 10);
                    else if (delta < -threshold) buy(targetCompany, 10);
                }
            }
        });
    }
}
