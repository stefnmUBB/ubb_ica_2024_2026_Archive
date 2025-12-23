using DPML_Proj1.CSP.Model;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Solvers
{
    /// <summary>
    /// A simple backtracking CSP solver that enumerates every possible
    /// full assignment of variable values and returns the first one that
    /// satisfies all constraints. No consistency propagation is used.
    /// </summary>
    public class BacktrackingSolver : CspSolver
    {
        public override CspSolution Solve(Problem problem, OperationControl opc)
        {
            var variables = problem.Variables;
            // One enumerator per variable's domain
            var enumeratorStates = problem.Variables.Select(var => var.Domain.Values.GetEnumerator()).ToArray();

            // Enumerate all complete assignments
            foreach (var candidate in EnumerateLabels(variables, enumeratorStates))
            {
                opc?.Check(); // allow cancellation/limit control
                OnCandidateInspected(candidate);
                if (problem.TestConstraints(candidate))
                {
                    return Success(candidate);  // found a satisfying assignment
                }
            }

            return Fail();
        }

        /// <summary>
        /// Enumerates all combinations of variable assignments by iterating
        /// their domain enumerators like a multi-digit counter.
        /// </summary>
        private static IEnumerable<CompoundLabel> EnumerateLabels(Variable[] variables, IEnumerator<Value>[] valueEnumerators)
        {
            // Initialize every enumerator to its first value
            foreach (var enumerator in valueEnumerators)
                ResetAndMoveNext(enumerator);

            while(true)
            {
                // Build the current assignment from each enumerator's Current value
                var values = valueEnumerators.Select(enumerator => enumerator.Current);
                yield return new CompoundLabel(variables.Zip(values, Label.Of).ToArray());

                // Multi-digit increment over the enumerators
                int k = 0;
                while(!valueEnumerators[k].MoveNext())
                {
                    // Reset exhausted enumerator and carry to the next one
                    ResetAndMoveNext(valueEnumerators[k++]);
                }
            }
        }

        /// <summary>
        /// Resets an enumerator and advances it to its first element.
        /// </summary>
        private static void ResetAndMoveNext<T>(IEnumerator<T> e)
        {
            e.Reset();
            e.MoveNext();
        }

    }
}
