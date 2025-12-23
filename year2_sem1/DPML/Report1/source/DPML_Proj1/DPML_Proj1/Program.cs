using DPML_Proj1.Core;
using DPML_Proj1.CSP.Model;
using DPML_Proj1.CSP.Reducers;
using DPML_Proj1.CSP.Solvers;
using DPML_Proj1.UI.Forms;
using System;
using System.Diagnostics;
using System.Windows.Forms;

namespace DPML_Proj1
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // very simple example on formal declaration of a problem 
            var problem = new ProblemBuilder()
                .Domain(Domain.IntRange(1, 5), out var dom)
                .Variable("x", dom, out var x)
                .Variable("y", dom, out var y)
                .Variable("z", dom, out var z)
                .Constraint(Constraint.Of(x, y).IntegerRelation((xVal, yVal) => xVal + yVal == 6))
                .Constraint(Constraint.Of(x, y).IntegerRelation((xVal, yVal) => xVal < yVal))
                .Constraint(Constraint.Of(z).IntegerRelation((zVal) => zVal > 3))
                .Build();

            // Instantiate the Zebra problem for test purposes
            problem = ProblemGeneratorTemplates.Riddle3H3N.GenerateProblem();

            // example on applying reducers and solve the problem
            var solution = problem
                .Reduce<NodeConsistencyReducer>()
                .Reduce<AC3Reducer>()
                .Reduce<GeneralizedArcConsistencyReducer>()
                .Solve<ForwardCheckingSolver>(onCandidateInspected: (label) => { Debug.WriteLine(label); })
                ;

            // finally print the solution
            Debug.WriteLine(solution);


            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }

}
