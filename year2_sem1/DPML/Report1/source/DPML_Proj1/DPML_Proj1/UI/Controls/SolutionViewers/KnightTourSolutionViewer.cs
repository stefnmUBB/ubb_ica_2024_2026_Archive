using DPML_Proj1.Core;
using DPML_Proj1.CSP.Model;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Controls.SolutionViewers
{
    public partial class KnightTourSolutionViewer : UserControl, ISolutionViewer
    {
        public KnightTourSolutionViewer()
        {
            InitializeComponent();
            DoubleBuffered = true;
        }

        private Bitmap RenderBitmap;

        int N, M;

        public void SetProblemGenerator(ProblemGenerator pgen)
        {
            N = pgen.GeParam<int>("N");
            M = pgen.GeParam<int>("M");

            RenderBitmap = new Bitmap(512, 512);

            DrawBitmap(null);
        }

        public void SetSolution(CompoundLabel solution)
        {
            DrawBitmap(solution);
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);

            lock (this)
            {
                if (IsRendering) return;

                var scale = Math.Min(1f * Width / RenderBitmap.Width, 1f * Height / RenderBitmap.Height);
                var newWidth = (int)(scale * RenderBitmap.Width);
                var newHeight = (int)(scale * RenderBitmap.Height);
                e.Graphics.DrawImage(RenderBitmap, (Width - newWidth) / 2, (Height - newHeight) / 2, newWidth, newHeight);
            }
        }

        private bool IsRendering = false;

        private void DrawBitmap(CompoundLabel solution)
        {
            // draw board layout

            lock (this)
            {
                IsRendering = true;
            }

            using (var g = Graphics.FromImage(RenderBitmap))
            {
                g.Clear(Color.Transparent);

                int bWidth = RenderBitmap.Width * 7 / 10;
                int bHeight = bWidth * N / M;

                int bLeft = (RenderBitmap.Width - bWidth) / 2;
                int bTop = (RenderBitmap.Height - bHeight) / 2;

                int cellSize = bWidth / M;

                for (int i = 0; i < N; i++)
                {
                    for (int j = 0; j < M; j++)
                    {
                        g.FillRectangle((i + j) % 2 == 0 ? Brushes.Olive : Brushes.DarkGoldenrod, bLeft + j * cellSize, bTop + i * cellSize, cellSize, cellSize);
                    }
                }

                for (int i = 0; i <= N; i++)
                {
                    int y = bTop + cellSize * i;
                    g.DrawLine(Pens.Black, bLeft, y, bLeft + bWidth, y);
                }

                for (int i = 0; i <= M; i++)
                {
                    int x = bLeft + cellSize * i;
                    g.DrawLine(Pens.Black, x, bTop, x, bTop + bHeight);
                }

                if (solution != null)
                {
                    var moves = new (int r, int c)[]
                    {
                        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)
                    };

                    using (var pen = new Pen(Color.Orange, 4f))
                    {
                        for (int i = 0; i < N; i++)
                        {
                            for (int j = 0; j < M; j++)
                            {
                                var next = solution.GetValueOrNull($"succ[{i},{j}]")?.EvaluateAs<int>() ?? -1;
                                if (next < 0) continue;

                                (var ni, var nj) = (next / M, next % M);

                                g.DrawLine(pen, bLeft + j * cellSize + cellSize / 2,
                                    bTop + i * cellSize + cellSize / 2,
                                    bLeft + nj * cellSize + cellSize / 2,
                                    bTop + ni * cellSize + cellSize / 2);
                            }
                        }
                    }
                }
            }

            lock (this)
            {
                IsRendering = false;
                Invalidate();
            }
        }
    }
}
