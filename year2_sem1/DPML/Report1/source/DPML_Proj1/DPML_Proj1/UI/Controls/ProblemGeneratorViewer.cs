using DPML_Proj1.Core;
using DPML_Proj1.UI.Controls.SolutionViewers;
using System;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Controls
{
    public partial class ProblemGeneratorViewer : UserControl
    {
        private Control Body = null;

        private readonly ProblemGenerator ProblemGenerator;

        public ProblemGeneratorViewer(ProblemGenerator problemGenerator)
        {
            InitializeComponent();
            ProblemGenerator = problemGenerator;

            DescriptionBox.Text = problemGenerator.Description;
        }

        protected override void OnHandleCreated(EventArgs e)
        {
            base.OnHandleCreated(e);

            if (!ProblemGenerator.HasParameters())
            {
                Task.Run(() =>
                {
                    var problem = ProblemGenerator.GenerateProblem();

                    Invoke(new Action(() =>
                    {
                        var solutionViewer = ProblemGenerator.SolutionViewerType != null
                            ? Activator.CreateInstance(ProblemGenerator.SolutionViewerType) as Control
                            : null;

                        (solutionViewer as ISolutionViewer)?.SetProblemGenerator(ProblemGenerator);

                        SetBody(new ProblemViewer(problem, solutionViewer));
                    }));
                });
            }
            else
            {
                Task.Run(() =>
                {
                    var problem = ProblemGenerator.GenerateProblem();

                    Invoke(new Action(() =>
                    {
                        var solutionViewer = ProblemGenerator.SolutionViewerType != null
                            ? Activator.CreateInstance(ProblemGenerator.SolutionViewerType) as Control
                            : null;

                        (solutionViewer as ISolutionViewer)?.SetProblemGenerator(ProblemGenerator);

                        SetBody(new ProblemViewer(problem, solutionViewer));
                    }));
                });
            }
        }


        private void SetBody(Control control)
        {
            if(Container!=null)
            {
                Controls.Remove(Body);
                Body = null;
            }
            if(control!=null)
            {
                control.Dock = DockStyle.Fill;
                Body = control;
                Controls.Add(Body);
                Body.BringToFront();
            }
        }

    }
}
