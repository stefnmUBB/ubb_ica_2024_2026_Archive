using DPML_Proj1.Core;
using DPML_Proj1.CSP.Model;
using DPML_Proj1.CSP.Solvers;
using System;
using System.Drawing;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Controls.SolutionViewers
{
    public partial class PicrossSolutionViewer : UserControl, ISolutionViewer
    {
        public PicrossSolutionViewer()
        {
            InitializeComponent();
            DoubleBuffered = true;
        }

        private Bitmap RenderBitmap;

        int N, M;
        int[][] RowCues, ColCues;


        public void SetProblemGenerator(ProblemGenerator pgen)
        {
            N = pgen.GeParam<int>("N");
            M = pgen.GeParam<int>("M");
            RowCues = pgen.GeParam<int[][]>("rowCues");
            ColCues = pgen.GeParam<int[][]>("colCues");

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

                for(int i=0;i<=N;i++)
                {
                    int y = bTop + cellSize * i;
                    g.DrawLine(Pens.Black, bLeft, y, bLeft+bWidth, y);
                }

                for (int i = 0; i <= M; i++)
                {
                    int x = bLeft + cellSize * i;
                    g.DrawLine(Pens.Black, x, bTop, x, bTop + bHeight);
                }

                if (solution != null)
                {
                    for (int i = 0; i < N; i++)
                    {
                        for (int j = 0; j < M; j++)
                        {
                            if ((solution.GetValueOrNull($"cell[{i},{j}]")?.EvaluateAs<int>() ?? 0) != 0) 
                            {
                                g.FillRectangle(Brushes.Blue, bLeft + j * cellSize, bTop + i * cellSize, cellSize, cellSize);
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
