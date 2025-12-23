using DPML_Proj1.CSP.Model;

namespace DPML_Proj1.CSP.Reducers
{
    public interface IReducer
    {
        /// <summary>
        /// Returns a new reduced Problem instance
        /// </summary>
        /// <param name="problem"></param>
        /// <returns></returns>
        Problem Reduce(Problem problem);
    }
}
