package org.example.demo;

import jade.core.behaviours.CyclicBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;

import java.util.HashMap;
import java.util.Map;

//----------------------------------------
// Info Trader Agent
//----------------------------------------
public class InfoTraderAgent extends TraderAgent {
    private Map<String, Double> trustLevels = new HashMap<>();

    protected void setup() {
        capital = 10000.0;

        // Register with DF
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
        sd.setType("event-subscriber");
        sd.setName("EventSubscriberService");
        dfd.addServices(sd);
        try {
            DFService.register(this, dfd);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }

        addBehaviour(new CyclicBehaviour() {
            public void action() {
                ACLMessage msg = receive();
                if (msg != null && msg.getPerformative() == ACLMessage.INFORM) {
                    String[] parts = msg.getContent().split(":");
                    String company = parts[0];
                    String event = parts[1];
                    double trust = trustLevels.getOrDefault(company, 0.5);
                    if (event.equals("success")) trust += 0.1;
                    else if (event.equals("fail")) trust -= 0.1;
                    trustLevels.put(company, Math.max(0.0, Math.min(1.0, trust)));

                    System.out.println("Info receives" + msg.getContent()+ ". Trust is "+trust);

                    if (trust > 0.7) buy(company, 5);
                    else if (trust < 0.3) sell(company, 5);
                } else {
                    block();
                }
            }
        });
    }
}
