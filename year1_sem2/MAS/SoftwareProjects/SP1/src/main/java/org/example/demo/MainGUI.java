package org.example.demo;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.util.*;
import java.util.stream.Collectors;

public class MainGUI extends Application {
    private final Map<String, Label> priceLabels = new HashMap<>();
    private final Map<String, Label> activityLabels = new HashMap<>();
    private Timer timer;
    private Plot2D pricePlot;
    private Plot2D tradePlot;
    private static final Color[] COLORS = {
        Color.BLUE, Color.RED, Color.GREEN, Color.PURPLE, Color.ORANGE
    };
    private final Map<String, Color> companyColors = new HashMap<>();
    private int colorIndex = 0;

    @Override
    public void start(Stage primaryStage) {
        VBox root = new VBox(12);
        root.setStyle("-fx-padding: 20; -fx-font-size: 14px;");

        Label header = new Label("Real-Time Stock Market");
        header.setStyle("-fx-font-size: 18px; -fx-font-weight: bold;");
        root.getChildren().add(header);

        // Initialize price plot
        Label priceChartTitle = new Label("Stock Price History");
        priceChartTitle.setStyle("-fx-font-weight: bold");
        root.getChildren().add(priceChartTitle);
          pricePlot = new Plot2D(600, 150);
        root.getChildren().add(pricePlot);

        // Initialize trade activity plot
        Label tradeChartTitle = new Label("Trade Activity History");
        tradeChartTitle.setStyle("-fx-font-weight: bold");
        root.getChildren().add(tradeChartTitle);
        
        tradePlot = new Plot2D(600, 150);
        root.getChildren().add(tradePlot);

        // Current values section
        Label currentTitle = new Label("Current Values");
        currentTitle.setStyle("-fx-font-weight: bold");
        root.getChildren().add(currentTitle);

        // Assign colors to companies
        for (String company : StockMarket.stockPrices.keySet()) {
            companyColors.put(company, COLORS[colorIndex % COLORS.length]);
            colorIndex++;
            
            Label label = new Label(company + ": $" + StockMarket.stockPrices.get(company));
            label.setStyle("-fx-text-fill: " + toWebColor(companyColors.get(company)));
            priceLabels.put(company, label);
            root.getChildren().add(label);
        }

        Separator agentSeparator = new Separator();
        root.getChildren().add(agentSeparator);

        Label agentsTitle = new Label("Agent Activity:");
        agentsTitle.setStyle("-fx-font-weight: bold;");
        root.getChildren().add(agentsTitle);

        // Add activity labels for each company
        for (String company : StockMarket.stockPrices.keySet()) {
            Label actLabel = new Label(company + ": waiting for data...");
            actLabel.setStyle("-fx-text-fill: " + toWebColor(companyColors.get(company)));
            activityLabels.put(company, actLabel);
            root.getChildren().add(actLabel);
        }

        Scene scene = new Scene(root, 650, 600);
        primaryStage.setScene(scene);
        primaryStage.setTitle("JADE Stock Simulation");
        primaryStage.show();

        // Start UI refresh
        timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                Platform.runLater(() -> {
                    updatePrices();
                    updateActivity();
                });
            }
        }, 0, 300);
    }    private String toWebColor(Color color) {
        return String.format("#%02X%02X%02X",
            (int) (color.getRed() * 255),
            (int) (color.getGreen() * 255),
            (int) (color.getBlue() * 255));
    }

    private void updatePrices() {
        pricePlot.clear();
        tradePlot.clear();

        for (String company : priceLabels.keySet()) {
            // Update price label
            double price = StockMarket.stockPrices.get(company);
            priceLabels.get(company).setText(company + ": $" + String.format("%.2f", price));            // Update price plot
            List<Double> prices = StockMarket.priceHistory.get(company);
            List<Double> times = StockMarket.timePoints.get(company);
            if (prices.size() == times.size()) {  // Ensure arrays are of equal length
                double[] xData = times.stream().mapToDouble(Double::doubleValue).toArray();
                double[] yData = prices.stream().mapToDouble(Double::doubleValue).toArray();
                pricePlot.plot(company, xData, yData, companyColors.get(company));

                // Update trade activity plot
                var tradesY = StockMarket.tradeCountHistory.get(company)
                        .stream().mapToDouble(Integer::doubleValue).toArray();
                var tradesX = StockMarket.tradeTimePoints.get(company)
                        .stream().mapToDouble(Double::doubleValue).toArray();

//                System.out.println(tradesX.length + ": " +
//                        Arrays.stream(tradesX)
//                                .mapToObj(Double::toString)
//                                .collect(Collectors.joining(", "))
//                );

//                System.out.println(tradesY.length + ": " +
//                        Arrays.stream(tradesY)
//                                .mapToObj(Double::toString)
//                                .collect(Collectors.joining(", "))
//                );

                tradePlot.plot(company, tradesX, tradesY, companyColors.get(company));


            }
        }
    }

    private void updateActivity() {
        for (String company : activityLabels.keySet()) {
            List<String> trades = StockMarket.tradeHistory.get(company);
            String summary = trades.isEmpty() ? "No trades" : trades.size() + " trades: " + String.join(", ", trades);
            activityLabels.get(company).setText(company + ": " + summary);
        }
    }

    @Override
    public void stop() {
        timer.cancel();
    }

    public static void main(String[] args) throws InterruptedException {
        // Launch JADE agents in parallel
        new Thread(() -> MainApp.main(args)).start();
        Thread.sleep(7000);
        launch(args);
    }
}
