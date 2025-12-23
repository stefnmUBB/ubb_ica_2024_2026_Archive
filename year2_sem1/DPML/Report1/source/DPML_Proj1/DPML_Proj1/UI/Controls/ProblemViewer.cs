using DPML_Proj1.CSP.Graphing;
using DPML_Proj1.CSP.Model;
using DPML_Proj1.CSP.Reducers;
using DPML_Proj1.CSP.Solvers;
using DPML_Proj1.UI.Controls.SolutionViewers;
using System;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Controls
{
    public partial class ProblemViewer : UserControl
    {
        private readonly Problem Problem;
        private ConstraintGraph ConstraintGraph = null;
        private Problem CurrentProblem;

        private Control SolutionViewer;

        public ProblemViewer(Problem problem, Control solutionViewer)
        {
            InitializeComponent();

            Problem = problem;
            SolutionViewer = solutionViewer;

            if(SolutionViewer!=null)
            {
                SolveContainer.Panel2.Controls.Add(SolutionViewer);
                SolutionViewer.Dock = DockStyle.Fill;
            }

        }

        protected override void OnHandleCreated(EventArgs e)
        {
            base.OnHandleCreated(e);

            SetCurrentProblem(Problem);
        }

        private void SetCurrentProblem(Problem problem)
        {
            CurrentProblem = problem;

            Task.Run(() =>
            {
                (var nodesCount, var edgesCount) = CurrentProblem.ComputeConstraintGraphSize();

                Invoke(new Action(() =>
                {
                    ProblemSizeLabel.Text = $"Nodes: {nodesCount}; Edges: {edgesCount}";
                }));
            });


            Task.Run(() =>
            {
                ConstraintGraph = ConstraintGraph ?? CurrentProblem.ComputeConstraintGraph();

                Invoke(new Action(() =>
                {
                    GraphViewer.Graph = ConstraintGraph;
                }));
            });
        }

        private bool IsSolverRunning = false;
        private OperationControl OperationControl = null;

        private void SolverButton_Click(object sender, EventArgs e)
        {
            var solverType = SolverSelector.SelectedItem as Type;

            if(IsSolverRunning)
            {
                OperationControl.Cancel();
                return;
            }


            OperationControl = new OperationControl();

            Task.Run(() =>
            {
                IsSolverRunning = true;
                Invoke(new Action(() => SolverButton.Text = "Stop"));


                var solver = Activator.CreateInstance(solverType) as ICspSolver;
                int labelsCount = 0;
                solver.CandidateInspected += (label) =>
                {
                    labelsCount++;
                    if(labelsCount%100==0)
                    {
                        Invoke(new Action(()=> (SolutionViewer as ISolutionViewer)?.SetSolution(label)));
                        Invoke(new Action(() => OutputBox.Text = $"Tested {labelsCount} candidates.{Environment.NewLine}{label}"));
                    }
                };

                try
                {
                    var solution = solver.Solve(CurrentProblem, OperationControl);
                    Invoke(new Action(() => (SolutionViewer as ISolutionViewer)?.SetSolution(solution.Solution)));

                    var outputText = "";

                    if (solution.IsSuccess)
                    {
                        outputText = $"Solution found after analyzing {labelsCount} candidates.{Environment.NewLine}{solution.Solution.ToString()}";
                    }
                    else
                    {
                        outputText = $"Could not find solution. Analyzed {labelsCount} candidates.{Environment.NewLine}{solution.Message}";
                    }

                    Invoke(new Action(() => OutputBox.Text = outputText));
                }
                catch(OperationCanceledException)
                {
                    Invoke(new Action(() => OutputBox.Text = "Canceled."));
                }

                IsSolverRunning = false;
                Invoke(new Action(() => SolverButton.Text = "Run"));
            });

        }

        private void SolverSelector_SelectedIndexChanged(object sender, EventArgs e)
        {
            var solverType = SolverSelector.SelectedItem as Type;
            SolverButton.Enabled = solverType != null;
        }

        private void ReduceButton_Click(object sender, EventArgs e)
        {
            Task.Run(() =>
            {
                void MeasureProblem(Problem p, string caption)
                {
                    TextboxWriteLine(ReducerOutputTextBox, caption);
                    var domainSizes = p.Variables.Select(v => v.Domain.Size).ToArray();

                    TextboxWriteLine(ReducerOutputTextBox, $"  Domain size: Avg={domainSizes.Average()}, Max={domainSizes.Max()}");
                    TextboxWriteLine(ReducerOutputTextBox, $"  Search space size: {domainSizes.Aggregate(1, (a, x) => a * x)}");


                }

                Invoke(new Action(() =>
                {
                    ReduceButton.Enabled = false;
                    ResetReduceButton.Enabled = false;
                }));

                var problem = CurrentProblem;

                MeasureProblem(problem, "Before reduce");

                foreach (var r in ReducerSelector.SelectedReducers.ToArray()) 
                {
                    problem = r.Reduce(problem);
                    MeasureProblem(problem, $"Reduced using {r.GetType().Name}");
                }

                Invoke(new Action(() => SetCurrentProblem(problem)));

                Invoke(new Action(() =>
                {
                    ReduceButton.Enabled = true;
                    ResetReduceButton.Enabled = true;
                }));
            });
        }

        private void ResetReduceButton_Click(object sender, EventArgs e)
        {
            SetCurrentProblem(Problem);
        }

        private void TextboxWriteLine(TextBox textbox, string message)
        {
            if (InvokeRequired)
            {
                textbox.Invoke(new Action(() => textbox.AppendText($"{message}{Environment.NewLine}")));
            }
            else
            {
                textbox.AppendText($"{message}{Environment.NewLine}");
            }
        }
    }
}
