using DPML_Proj1.CSP.Model;
using System;

namespace DPML_Proj1.CSP.Solvers
{
    public static class ProblemExtensions
    {
        public static CspSolution Solve<S>(
            this Problem problem,
            Action<CompoundLabel> onCandidateInspected = null
            ) where S : ICspSolver, new()
        {
            var solver = new S();
            if (onCandidateInspected != null)
            {
                solver.CandidateInspected += (l) => onCandidateInspected(l);
            }
            return solver.Solve(problem);
        }
    }
}
