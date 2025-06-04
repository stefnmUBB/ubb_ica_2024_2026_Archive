package org.example.demo;

import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.ContainerController;

import java.util.List;

//----------------------------------------
// Main Application
//----------------------------------------
public class MainApp {
    public static void main(String[] args) {
        Runtime rt = Runtime.instance();
        Profile p = new ProfileImpl();
        ContainerController cc = rt.createMainContainer(p);

        List<String> companies = List.of("C1", "C2");
        StockMarket.initStocks(companies, 100.0);

        try {
            for (String c : companies) {
                cc.createNewAgent(c, "org.example.demo.CompanyAgent", null).start();
            }
            cc.createNewAgent("org.example.demo.Regulator", "org.example.demo.RegulatorAgent", null).start();
            cc.createNewAgent("org.example.demo.InfoTrader", "org.example.demo.InfoTraderAgent", null).start();
            cc.createNewAgent("org.example.demo.TrendTrader", "org.example.demo.TrendTraderAgent", null).start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
