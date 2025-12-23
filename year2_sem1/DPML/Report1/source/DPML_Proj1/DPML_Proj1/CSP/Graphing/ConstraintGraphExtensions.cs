using DPML_Proj1.CSP.Model;

namespace DPML_Proj1.CSP.Graphing
{
    public static class ConstraintGraphExtensions
    {
        public static (int NodesCount, int EdgesCount) ComputeConstraintGraphSize(this Problem problem) 
            => ConstraintGraph.ComputeConstraintGraphSize(problem);

        public static ConstraintGraph ComputeConstraintGraph(this Problem problem)
            => ConstraintGraph.FromProblem(problem);
    }
}
