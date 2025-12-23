using DPML_Proj1.Core;
using DPML_Proj1.CSP.Model;
using DPML_Proj1.CSP.Solvers;

namespace DPML_Proj1.UI.Controls.SolutionViewers
{
    public interface ISolutionViewer
    {
        void SetProblemGenerator(ProblemGenerator pgen);

        void SetSolution(CompoundLabel solution);
    }
}
