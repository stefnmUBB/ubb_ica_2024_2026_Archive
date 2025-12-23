using DPML_Proj1.CSP.Model;

namespace DPML_Proj1.CSP.Reducers
{
    public static class ProblemExtensions
    {
        public static Problem Reduce<R>(this Problem problem) where R:IReducer, new()
        {
            return new R().Reduce(problem);
        }
    }
}
