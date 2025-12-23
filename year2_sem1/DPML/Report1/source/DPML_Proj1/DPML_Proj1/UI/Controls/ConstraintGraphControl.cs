using System;
using System.Collections.Generic;
using System.Linq;
using DPML_Proj1.CSP.Graphing;
using System.Drawing;
using System.Windows.Forms;
using DPML_Proj1.CSP.Model;

namespace DPML_Proj1.UI.Controls
{

    public class ConstraintGraphControl : Control
    {
        public ConstraintGraph Graph { get; set; }

        private Dictionary<Variable, PointF> nodePositions = new Dictionary<Variable, PointF>();
        private const int NodeRadius = 12;
        private const int Iterations = 400;
        private const float SpringLength = 100f;
        private const float Repulsion = 10000f;
        private bool layoutComputed = false;

        private Variable draggingNode = null;
        private PointF dragOffset;
        private bool draggingView = false;
        private PointF lastMouse;
        private PointF graphOffset = new PointF(0, 0);

        public ConstraintGraphControl()
        {
            DoubleBuffered = true;

            MouseDown += OnMouseDown;
            MouseMove += OnMouseMove;
            MouseUp += OnMouseUp;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            if (Graph == null) return;

            if (!layoutComputed)
            {
                ComputeLayout();
                layoutComputed = true;
            }

            var g = e.Graphics;
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

            // Apply translation (panning)
            g.TranslateTransform(graphOffset.X, graphOffset.Y);

            // Draw edges
            using (var pen = new Pen(Color.Gray, 1.8f))
            {
                foreach (var edge in Graph.Edges)
                {
                    if (nodePositions.ContainsKey(edge.From) && nodePositions.ContainsKey(edge.To))
                        g.DrawLine(pen, nodePositions[edge.From], nodePositions[edge.To]);
                }
            }

            // Draw nodes and labels
            using (var brush = new SolidBrush(Color.LightBlue))
            using (var border = new Pen(Color.Black, 1.8f))
            using (var font = new Font("Segoe UI", 9))
            using (var sf = new StringFormat { Alignment = StringAlignment.Center })
            {
                foreach (var node in Graph.Nodes)
                {
                    if (!nodePositions.ContainsKey(node)) continue;
                    var pos = nodePositions[node];

                    g.DrawString(node.Name, font, Brushes.Black,
                        new PointF(pos.X, pos.Y - NodeRadius - 14), sf);

                    g.FillEllipse(brush, pos.X - NodeRadius, pos.Y - NodeRadius, NodeRadius * 2, NodeRadius * 2);
                    g.DrawEllipse(border, pos.X - NodeRadius, pos.Y - NodeRadius, NodeRadius * 2, NodeRadius * 2);
                }
            }
        }

        private void ComputeLayout()
        {
            if (Graph.Nodes.Length == 0) return;

            var rnd = new Random();
            int width = ClientSize.Width;
            int height = ClientSize.Height;

            nodePositions.Clear();
            foreach (var node in Graph.Nodes)
                nodePositions[node] = new PointF(rnd.Next(NodeRadius, width - NodeRadius),
                                                 rnd.Next(NodeRadius, height - NodeRadius));

            for (int iter = 0; iter < Iterations; iter++)
            {
                var displacements = Graph.Nodes.ToDictionary(n => n, n => new PointF(0, 0));

                // Repulsion
                for (int i = 0; i < Graph.Nodes.Length; i++)
                {
                    for (int j = i + 1; j < Graph.Nodes.Length; j++)
                    {
                        var u = Graph.Nodes[i];
                        var v = Graph.Nodes[j];
                        var dx = nodePositions[u].X - nodePositions[v].X;
                        var dy = nodePositions[u].Y - nodePositions[v].Y;
                        var dist2 = dx * dx + dy * dy;
                        if (dist2 < 0.01f) dist2 = 0.01f;
                        var dist = (float)Math.Sqrt(dist2);

                        var force = Repulsion / dist2;
                        var fx = force * dx / dist;
                        var fy = force * dy / dist;

                        displacements[u] = new PointF(displacements[u].X + fx, displacements[u].Y + fy);
                        displacements[v] = new PointF(displacements[v].X - fx, displacements[v].Y - fy);
                    }
                }

                // Attraction
                foreach (var edge in Graph.Edges)
                {
                    var u = edge.From;
                    var v = edge.To;
                    var dx = nodePositions[u].X - nodePositions[v].X;
                    var dy = nodePositions[u].Y - nodePositions[v].Y;
                    var dist = (float)Math.Sqrt(dx * dx + dy * dy);
                    if (dist < 0.01f) dist = 0.01f;

                    var force = (dist - SpringLength) * 0.1f;
                    var fx = force * dx / dist;
                    var fy = force * dy / dist;

                    displacements[u] = new PointF(displacements[u].X - fx, displacements[u].Y - fy);
                    displacements[v] = new PointF(displacements[v].X + fx, displacements[v].Y + fy);
                }

                // Apply
                foreach (var node in Graph.Nodes)
                {
                    var pos = nodePositions[node];
                    pos.X += Math.Max(-5, Math.Min(5, displacements[node].X));
                    pos.Y += Math.Max(-5, Math.Min(5, displacements[node].Y));
                    nodePositions[node] = pos;
                }
            }

            // Reset panning offset
            graphOffset = new PointF(0, 0);
        }

        // === Mouse interaction ===
        private void OnMouseDown(object sender, MouseEventArgs e)
        {
            if (Graph == null) return;

            PointF p = ScreenToGraph(e.Location);

            foreach (var node in Graph.Nodes)
            {
                if (!nodePositions.ContainsKey(node)) continue;
                var pos = nodePositions[node];
                var dx = p.X - pos.X;
                var dy = p.Y - pos.Y;
                if (dx * dx + dy * dy <= NodeRadius * NodeRadius)
                {
                    draggingNode = node;
                    dragOffset = new PointF(dx, dy);
                    Capture = true;
                    return;
                }
            }

            // otherwise start view panning
            draggingView = true;
            lastMouse = e.Location;
            Capture = true;
        }

        private void OnMouseMove(object sender, MouseEventArgs e)
        {
            if (draggingNode != null)
            {
                nodePositions[draggingNode] = ScreenToGraph(new PointF(e.X - dragOffset.X, e.Y - dragOffset.Y));
                Invalidate();
            }
            else if (draggingView)
            {
                var dx = e.X - lastMouse.X;
                var dy = e.Y - lastMouse.Y;
                graphOffset = new PointF(graphOffset.X + dx, graphOffset.Y + dy);
                lastMouse = e.Location;
                Invalidate();
            }
        }

        private void OnMouseUp(object sender, MouseEventArgs e)
        {
            draggingNode = null;
            draggingView = false;
            Capture = false;
        }

        private PointF ScreenToGraph(PointF p)
        {
            return new PointF(p.X - graphOffset.X, p.Y - graphOffset.Y);
        }
    }

}
