using DPML_Proj1.CSP.Model;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Reducers
{
    /// <summary>
    /// Enforces node consistency by removing from each variable's domain
    /// any value that violates its unary constraints. Only constraints that
    /// involve a single variable are considered.
    /// </summary>
    public class NodeConsistencyReducer : IReducer
    {
        public Problem Reduce(Problem problem)
        {
            var newVars = new List<Variable>();
            foreach (var v in problem.Variables)
            {
                // Keep only values that satisfy all unary constraints on v
                var newDomain = v.Domain.Values
                    .Where(val =>
                    {
                        var label = new CompoundLabel(Label.Of(v, val));
                        return problem.Constraints
                            .Where(c => c.IsUnaryConstraintOf(v))
                            .All(c => c.Evaluate(label));
                    });
                // Create the updated variable with its pruned domain
                newVars.Add(new Variable(v.Name, new Domain(newDomain)));
            }

            // Rebind constraints to the updated variable instances
            var constraints = problem.Constraints
                .Select(constraint => constraint.ReplaceVariablesByName(newVars))
                .ToArray();

            // Return the reduced CSP
            return new Problem(newVars.ToArray(), constraints);
        }
    }
}
