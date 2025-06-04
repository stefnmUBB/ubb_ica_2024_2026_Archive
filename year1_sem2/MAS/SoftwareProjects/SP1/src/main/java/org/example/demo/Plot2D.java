package org.example.demo;

import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Control;
import javafx.scene.layout.Region;
import javafx.scene.paint.Color;
import java.util.*;

public class Plot2D extends Region {
    private final Canvas canvas;
    private final Map<String, List<Point2D>> datasets;
    private final Map<String, Color> colors;
    private double minX = Double.MAX_VALUE;
    private double maxX = Double.MIN_VALUE;
    private double minY = Double.MAX_VALUE;
    private double maxY = Double.MIN_VALUE;
    private double padding = 40;
    private boolean hasData = false;

    private static class Point2D {
        double x, y;
        Point2D(double x, double y) {
            this.x = x;
            this.y = y;
        }
    }

    public Plot2D() {
        this(400, 300); // Default size
    }

    public Plot2D(double width, double height) {
        canvas = new Canvas(width, height);
        datasets = new HashMap<>();
        colors = new HashMap<>();
        getChildren().add(canvas);

        // Bind canvas size to region size
        canvas.widthProperty().bind(widthProperty());
        canvas.heightProperty().bind(heightProperty());

        // Redraw when size changes
        canvas.widthProperty().addListener((obs, old, newVal) -> redraw());
        canvas.heightProperty().addListener((obs, old, newVal) -> redraw());
    }

    public void clear() {
        datasets.clear();
        colors.clear();
        minX = Double.MAX_VALUE;
        maxX = Double.MIN_VALUE;
        minY = Double.MAX_VALUE;
        maxY = Double.MIN_VALUE;
        hasData = false;
        redraw();
    }

    public void plot(String name, double[] x, double[] y) {
        plot(name, x, y, Color.BLUE);
    }

    public void plot(String name, double[] x, double[] y, Color color) {
        if (x.length != y.length) {
            throw new IllegalArgumentException("X and Y arrays must have the same length");
        }

        List<Point2D> points = new ArrayList<>();
        for (int i = 0; i < x.length; i++) {
            points.add(new Point2D(x[i], y[i]));
            minX = Math.min(minX, x[i]);
            maxX = Math.max(maxX, x[i]);
            minY = Math.min(minY, y[i]);
            maxY = Math.max(maxY, y[i]);
        }

        datasets.put(name, points);
        colors.put(name, color);
        hasData = true;
        redraw();
    }

    private void redraw() {
        GraphicsContext gc = canvas.getGraphicsContext2D();
        gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());

        if (!hasData) return;

        double plotWidth = canvas.getWidth() - 2 * padding;
        double plotHeight = canvas.getHeight() - 2 * padding;

        // Draw axes
        gc.setStroke(Color.BLACK);
        gc.setLineWidth(1);
        gc.strokeLine(padding, canvas.getHeight() - padding, canvas.getWidth() - padding, canvas.getHeight() - padding); // X axis
        gc.strokeLine(padding, padding, padding, canvas.getHeight() - padding); // Y axis

        // Draw axis labels
        gc.strokeText(String.format("%.2f", minX), padding, canvas.getHeight() - padding / 2);
        gc.strokeText(String.format("%.2f", maxX), canvas.getWidth() - padding, canvas.getHeight() - padding / 2);
        gc.strokeText(String.format("%.2f", minY), padding / 2, canvas.getHeight() - padding);
        gc.strokeText(String.format("%.2f", maxY), padding / 2, padding);

        // Draw legend
        double legendX = canvas.getWidth() - padding - 100;
        double legendY = padding;
        for (Map.Entry<String, Color> entry : colors.entrySet()) {
            gc.setStroke(entry.getValue());
            gc.strokeLine(legendX, legendY, legendX + 20, legendY);
            gc.setStroke(Color.BLACK);
            gc.strokeText(entry.getKey(), legendX + 25, legendY + 5);
            legendY += 20;
        }

        // Plot data
        for (Map.Entry<String, List<Point2D>> entry : datasets.entrySet()) {
            List<Point2D> points = entry.getValue();
            gc.setStroke(colors.get(entry.getKey()));
            gc.setLineWidth(2);

            for (int i = 1; i < points.size(); i++) {
                Point2D p1 = points.get(i - 1);
                Point2D p2 = points.get(i);
                
                double x1 = padding + (p1.x - minX) * plotWidth / (maxX - minX);
                double y1 = canvas.getHeight() - padding - (p1.y - minY) * plotHeight / (maxY - minY);
                double x2 = padding + (p2.x - minX) * plotWidth / (maxX - minX);
                double y2 = canvas.getHeight() - padding - (p2.y - minY) * plotHeight / (maxY - minY);
                
                gc.strokeLine(x1, y1, x2, y2);
            }
        }
    }    @Override
    protected void layoutChildren() {
        // No need to set width/height as they are bound
        canvas.setLayoutX(0);
        canvas.setLayoutY(0);
    }

    @Override
    protected double computePrefWidth(double height) {
        return 400;
    }

    @Override
    protected double computePrefHeight(double width) {
        return 300;
    }
    
    @Override 
    protected double computeMinWidth(double height) {
        return 200;
    }
    
    @Override
    protected double computeMinHeight(double width) {
        return 150;
    }
}
