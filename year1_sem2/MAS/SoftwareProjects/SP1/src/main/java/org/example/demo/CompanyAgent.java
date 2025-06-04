package org.example.demo;

import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;

import java.util.Random;

//----------------------------------------
// Company Agent
//----------------------------------------
public class CompanyAgent extends Agent {
    private Random rand = new Random();
    private String companyName;
    private String lastProject = "risk";

    protected void setup() {
        companyName = getLocalName();

        addBehaviour(new TickerBehaviour(this, 5000) {
            protected void onTick() {
                ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
                msg.setContent(companyName + ":" + lastProject);
                System.out.println("Company" + companyName + " announces " + msg.getContent());

                try {
                    DFAgentDescription template = new DFAgentDescription();
                    ServiceDescription sd = new ServiceDescription();
                    sd.setType("event-subscriber");
                    template.addServices(sd);
                    DFAgentDescription[] result = DFService.search(myAgent, template);

                    for (DFAgentDescription dfd : result) {
                        msg.addReceiver(dfd.getName());
                    }
                    send(msg);
                } catch (FIPAException fe) {
                    fe.printStackTrace();
                }

                // update last project
                int chance = rand.nextInt(3);
                if (chance == 0) lastProject = "success";
                else if (chance == 1) lastProject = "fail";
                else lastProject = "risk";
            }
        });
    }
}
