using DPML_Proj1.CSP.Model;

namespace DPML_Proj1.CSP.Solvers
{
    /// <summary>
    /// Solution to a CSP problem, handles either success or failure.
    /// Containts the compund label that satisfies the problem, or an error message
    /// explaining why it was not successful
    /// </summary>
    public class CspSolution
    {
        public readonly bool IsSuccess;
        public readonly CompoundLabel Solution;
        public readonly string Message;

        private CspSolution(bool isSuccess, CompoundLabel solution, string message)
        {
            IsSuccess = isSuccess;
            Solution = solution;
            Message = message;
        }

        public static CspSolution Success(CompoundLabel solution) => new CspSolution(true, solution, null);
        public static CspSolution Fail(string message) => new CspSolution(false, null, message);

        public override string ToString()
        {
            if(IsSuccess)
            {
                return $"Success({Solution})";
            }
            return $"Fail({Message})";
        }

    }

    /// <summary>
    /// Event handler to pick on which (partial) solutions were evaluated 
    /// </summary>
    /// <param name="label"></param>
    public delegate void OnCandidateInspected(CompoundLabel label);

    /// <summary>
    /// Works like a CancellationToken, allows the user to stop the solver
    /// from another thread. Useful when the solver takes too long and we want to quit it. 
    /// </summary>
    public class OperationControl
    {
        private bool IsCancelled = false;

        public void Cancel()
        {
            lock(this) { IsCancelled = true; }
        }

        public void Check()
        {
            lock(this)
            {
                if(IsCancelled)
                {
                    throw new System.OperationCanceledException();
                }
            }
        }
    }

    public interface ICspSolver
    {
        /// <summary>
        /// Given the CSP problem, return a solution for it
        /// </summary>
        /// <param name="problem"></param>
        /// <param name="opc"></param>
        /// <returns></returns>
        CspSolution Solve(Problem problem, OperationControl opc = null);

        event OnCandidateInspected CandidateInspected;
    }

    public abstract class CspSolver : ICspSolver
    {
        /// <returns></returns>
        public abstract CspSolution Solve(Problem problem, OperationControl opc = null);

        // helper members to use in derived classes
        protected CspSolution Success(CompoundLabel solution) => CspSolution.Success(solution);
        protected CspSolution Fail(string message = "Could not find solution") => CspSolution.Fail(message);

        public event OnCandidateInspected CandidateInspected;

        protected void OnCandidateInspected(CompoundLabel label)
        {
            CandidateInspected?.Invoke(label);
        }
    }

}
