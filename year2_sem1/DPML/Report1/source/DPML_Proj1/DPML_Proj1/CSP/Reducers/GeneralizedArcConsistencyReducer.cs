using DPML_Proj1.CSP.Model;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Reducers
{
    /// <summary>
    /// Enforces Generalized Arc Consistency (GAC) across all constraints,
    /// removing domain values that cannot be extended to a full assignment
    /// satisfying the constraints they participate in. Works with constraints
    /// with any number of variables.
    /// </summary>
    public class GeneralizedArcConsistencyReducer : IReducer
    {
        public Problem Reduce(Problem problem)
        {
            // Clone variable domains for modification
            var domains = problem.Variables.ToDictionary(v => v, v => v.Domain.Values.ToList());

            // Cache support table: (Variable, Value, Constraint) -> whether it has at least one support
            var supportTable = new Dictionary<(Variable, Value, Constraint), bool>();

            bool changed;
            do
            {
                changed = false;
                // For every constraint in the problem
                foreach (var constraint in problem.Constraints)
                {
                    // For every variable appearing in the constraint
                    foreach (var v in constraint.Variables)
                    {
                        var domain = domains[v];
                        var toRemove = new List<Value>();

                        // Check each value of the variable
                        foreach (var value in domain)
                        {
                            var key = (v, value, constraint);

                            if (supportTable.TryGetValue(key, out bool supported))
                            {
                                // Reuse cached support result if available, nothing to compute if we find it
                            }
                            else
                            {
                                // if it doesn't exist, check if support exists and remember the result 
                                supported = ExistsSupport(v, value, constraint, domains);
                                supportTable[key] = supported;
                            }

                            if (!supported)
                                toRemove.Add(value);
                        }

                        // Remove all unsupported values from the domain
                        if (toRemove.Count > 0)
                        {
                            domains[v].RemoveAll(toRemove.Contains);
                            changed = true;
                        }
                    }
                }
            } while (changed);

            // Build reduced problem with updated domains
            var reducedVars = problem.Variables
                .Select(v => new Variable(v.Name, new Domain(domains[v])))
                .ToArray();

            var constraints = problem.Constraints
                .Select(c => c.ReplaceVariablesByName(reducedVars))
                .ToArray();

            return new Problem(reducedVars, constraints);
        }

        /// <summary>
        /// Checks whether 'value' of variable 'target' has at least one supporting
        /// assignment of the other variables in the constraint, using their current domains.
        /// </summary>
        private bool ExistsSupport(
            Variable target,
            Value value,
            Constraint constraint,
            Dictionary<Variable, List<Value>> domains)
        {
            var vars = constraint.Variables;
            var otherVars = vars.Where(v => v != target).ToArray();

            // Cartesian product of the domains of other variables
            IEnumerable<IEnumerable<Value>> product = CartesianProduct(otherVars.Select(v => domains[v]));

            // For each tuple of values, check whether assigning them satisfies the constraint
            foreach (var tuple in product)
            {
                var labels = new List<Label> { Label.Of(target, value) };
                labels.AddRange(otherVars.Zip(tuple, Label.Of));

                var label = new CompoundLabel(labels.ToArray());
                if (constraint.Evaluate(label))
                    return true;
            }

            return false;
        }

        /// <summary>
        /// Computes the Cartesian product of sequences of values.
        /// </summary>
        private static IEnumerable<IEnumerable<T>> CartesianProduct<T>(IEnumerable<IEnumerable<T>> sequences)
        {
            IEnumerable<IEnumerable<T>> result = new[] { Enumerable.Empty<T>() };
            foreach (var seq in sequences)
            {
                result = result.SelectMany(
                    prev => seq,
                    (prev, item) => prev.Append(item));
            }
            return result;
        }
    }
}
